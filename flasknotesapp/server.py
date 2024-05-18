""" Main Server Page  """
import os
import io
import sqlite3
import json
import urllib
import flask
import requests
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
    make_response,
    send_file
)
from flask_login import login_required, login_user, logout_user, LoginManager
from flask_wtf import FlaskForm
from waitress import serve
from wtforms import FileField, SubmitField
from databases import user_database
from objects.user import User
from objects.file_classes import File
from objects.onedrive import GRAPH_API_ENDPOINT

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["UPLOAD_FOLDER"] = "static\\files"
app.secret_key = """Generate Secret Key"""

login_manager = LoginManager()
login_manager.init_app(app)


def copy_file_to_favorites(headers, file_id, favorites_folder_id):
    """
    copy a file to the 'Favorites' folder in OneDrive.

    :param headers: Authorization headers.
    :param file_id: ID of the file to move.
    :param favorites_folder_id: ID of the 'Favorites' folder.
    :return: JSON response from the OneDrive API.
    """
    copy_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/copy"
    body = {
        "parentReference": {
            "id": favorites_folder_id
        }
    }
    response = requests.post(copy_url, headers=headers, json=body, timeout=30)
    response.raise_for_status()


def copy_file_to_favorites_shared(headers, file_id, favorites_folder_id):
    """
    copy a file to the 'Favorites' folder in OneDrive from a shared folder.

    :param headers: Authorization headers.
    :param file_id: ID of the file to move.
    :param favorites_folder_id: ID of the 'Favorites' folder.
    :return: JSON response from the OneDrive API.
    """
    ids_split = file_id.split(",")
    driveid = ids_split[1]
    fileid = ids_split[0]
    # /drives/{driveId}/items/{itemId}/copy
    # copy_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/copy"
    copy_url = f"https://graph.microsoft.com/v1.0/drives/{driveid}/items/{fileid}/copy"
    body = {
        "parentReference": {
            "id": favorites_folder_id
        }
    }
    response = requests.post(copy_url, headers=headers, json=body, timeout=30)
    response.raise_for_status()


@login_manager.user_loader
def load_user(user_id):
    """Load a user object from the database given its user ID.

    Parameters:
    user_id (int): the User_ID given to each of the users.

    Returns:
    User or None: User object which is the same user with that ID.
    None: object doesn't exist.
    """

    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()
    cursor.execute(
        """SELECT user_id, username, password,
        email FROM user where (user_id = ?)""",
        (user_id,),
    )
    row = cursor.fetchall()
    connection.close()
    if len(row) == 1:
        return User(row[0][0], row[0][1], row[0][2], row[0][3])
    return None


def checkdatabase():
    """calls the function that creates the database from the user_database file.
    Parameters:
    None.
    Returns:
    None.
    """
    user_database.create_database()


@app.route("/")
def set_up():
    """Sets up the loginpage to set up the flask project.

    Parameters:
    None.

    Returns:
    flask method: render_template with String loginpage.html.
    """
    return render_template("loginpage.html")


@app.route("/form_login", methods=["POST"])
def login():
    """Handles the user login functionality.
    Parameters:
    None.
    Returns:
    flask method: that redirects to homepage or render_template
    with loginpage.html and the errors messages with it.
    Source: adapted from https://www.scaler.com/topics/login-page-in-html/
    Souces: adapted this https://www.youtube.com/watch?v=R-hkzqjRMwM&ab_channel=NachiketaHebbar
    """

    get_name = request.form["username"]
    get_password = request.form["password"]
    current_user = User(None, get_name, get_password, None)
    if current_user.is_authenticated():
        flask.flash("Logged in successfully.")
        current_user.set_login_user_id()
        current_user.set_login_email()
        login_user(current_user)
        # next = flask.request.args.get('next')
        session["username"] = (
            get_name  # set the session key for getting the One Drive header
        )
        return redirect(url_for("homepage"))
    error_message = "Incorrect Username or Password!"
    return render_template("loginpage.html", msg=error_message)


@app.route("/homepage")
@login_required
def homepage():
    """Loads the homepage.

    Parameters:
    None.

    Returns:
    Flask method with homepage.html.
    """

    return render_template("homepage.html")


@app.route("/register")
def register():
    """Loads the register page.

    Parameters:
    None.

    Returns:
    flask method that has the register.html page.
    """

    return render_template("register.html")


@app.route("/form_register", methods=["POST", "GET"])
def register_actions():
    """Handles the register form and adds the user to database.
    Parameters:
    None.
    Returns:
    flask method with register.html with the error messages or
    flask method with homepage.html.
    Sources: Adapted from https://www.scaler.com/topics/login-page-in-html/
    Souces: adapted this https://www.youtube.com/watch?v=R-hkzqjRMwM&ab_channel=NachiketaHebbar
    """
    get_email = request.form["email"]
    get_name = request.form["username"]
    get_password = request.form["password"]
    get_confirmpassword = request.form["confirmpassword"]
    new_user = User(None, get_name, get_password, get_email)
    (
        username_message,
        email_message,
        password_message,
        confirm_password_message,
        register_status,
    ) = new_user.check_new_user(get_confirmpassword)

    if register_status is False:
        return render_template(
            "register.html",
            email_error=email_message,
            username_error=username_message,
            password_error=password_message,
            confirm_password_error=confirm_password_message,
        )
    flask.flash("Logged in successfully.")
    login_user(new_user)
    return render_template("homepage.html")


@app.route("/forgotpsd")
def forgot_password():
    """Function that loads the forgot password page.

    Parameters:
    None.

    Returns:
    Flask method that has the 'forgot_pswd.html' page.
    """
    return render_template("forgot_pswd.html")


class UploadFileForm(FlaskForm):
    """Summary: Gives the file that is uploaded
    Parameters: specified formdata
    Returns: uploaded file
    object: User
    None
    """
    file = FileField("File")
    submit = SubmitField("Upload File")

    def method1(self):
        """Placeholder method 1."""
        # placeholder
        print("Method 1")

    def method2(self):
        """Placeholder method 2."""
        # placeholder
        print("Method 2")


@app.route("/upload", methods=["POST"])
@login_required
def upload_page_setup():
    """Uploads a file to OneDrive"""
    group = request.form["title"]
    form = UploadFileForm()
    return render_template("upload.html", form=form, group=group)


@app.route("/upload_page_action", methods=["GET", "POST"])
@login_required
def upload_page_action():
    """Summary:
    Sources: https://www.youtube.com/watch?v=Ok8O_QnrSBI&ab_channel=JieJenn
    """
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    group = request.form["group"]
    #  Use request.files to access uploaded files (chatgpt helped get the files part)
    file = request.files["file"]
    timeout = 60
    if file:
        response = requests.put(
            GRAPH_API_ENDPOINT
            + f"/me/drive/items/root:/{group}/{file.filename}:/content",
            headers=headers,
            data=file.read(),  # Use file.read() to get the file content
            timeout=timeout,
        )
        if response == 400:
            return onedrive()

    return get_my_folders()


@app.route("/upload_page_setup_shared", methods=["POST"])
@login_required
def upload_page_setup_shared():
    """Uploads a file to OneDrive"""
    group = request.form["title"]
    file_id = request.form["file_id"]
    form = UploadFileForm()
    return render_template(
        "upload_shared.html", form=form, group=group, file_id=file_id
    )


@app.route("/upload_page_action_shared", methods=["GET", "POST"])
@login_required
def upload_page_action_shared():
    """Summary:
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    Soueces: Also used: https://learn.microsoft.com/en-us/onedrive/developer/
    rest-api/api/driveitem_createlink?view=odsp-graph-online
    """
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    #  group = request.form["group"]
    current_folder_ids = request.form["file_id"]
    ids_split = current_folder_ids.split(",")
    drive_id = ids_split[0]
    remote_id = ids_split[1]
    file = request.files["file"]
    timeout = 60
    new_url = f"/drives/{drive_id}/items/{remote_id}:/{file.filename}:/content"
    if file:
        response = requests.put(
            url + new_url,
            headers=headers,
            data=file.read(),  # Use file.read() to get the file content
            timeout=timeout,
        )
    if response == 400:
        return onedrive()
    return get_shared_folders()


@app.route("/group")
@login_required
def group_page():
    """Render the group page.

    This function renders the 'groups.html' template, which represents the group creation page.

    Returns:
    rendered_template: HTML content of the rendered template.
    """
    return render_template("groups.html")


@app.route("/group_details")
@login_required
def group_details_page():
    """
    Render the group details page.

    This function retrieves the value of the 'title' query parameter from the request.
    If the parameter is not provided, it defaults to 'Default Group Name'.
    The function then renders the 'group_details.html' template, passing the retrieved group name.

    Returns:
    rendered_template: HTML content of the rendered template.
    """
    group_name = request.args.get("title", "Default Group Name")
    return render_template("group_details.html", group_name=group_name)


@app.route("/logout")
@login_required
def logoutpage_page():
    """Summary or Description of the function

    Parameters:

    Returns:
    """

    if os.path.exists("ms_graph_api_token.json"):
        os.remove("ms_graph_api_token.json")
    else:
        pass
    return redirect(url_for("logout_method"))


@app.route("/logout_method")
def logout_method():
    """Summary or Description of the function

    Parameters:

    Returns:
    object: User
    None.
    """

    logout_user()
    return render_template("logoutpage.html")


@app.route("/show_message")
def show_message():
    '''Summary: renders template for show_message
    '''
    return render_template("show_message.html")


@app.route("/onedrive")
@login_required
def onedrive():
    """Summary or Description of the function
    Authenticates with onedrive account
    Parameters:
    None
    Returns: headers to access onedrive account
    object: User
    None
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    """
    client_id = "Create Your Own Client ID"
    permissions = ["Files.ReadWrite"]
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    response_type = 'token'
    redirect_uri = 'https://localhost:8000/onedrive_message'
    scope = ""
    for index, permission in enumerate(permissions):
        scope += permission
        if index < len(permissions) - 1:
            scope += "+"
    url = url + '?client_id=' + client_id + '&scope=' + scope + '&response_type=' \
        + response_type + '&redirect_uri=' + urllib.parse.quote(redirect_uri)
    return render_template("onedrive.html", url=url, scope=scope)


@app.route('/onedrive_message')
def onedrive_message():
    '''
    Summary: Message that will be displayed when user authenticates
    '''
    return render_template("message.html")


@app.route("/", methods=["POST"])
@login_required
def get_token():
    ''' Gets the token
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    '''
    code = request.form.get("info_url")
    token = code[(code.find('access_token') + len('access_token') + 1): (code.find('&token_type'))]
    url = 'https://graph.microsoft.com/v1.0/'
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url + 'me/drive/', headers=headers, timeout=30)
    if response.status_code == 200:
        response = json.loads(response.text)
        print('Connected to the OneDrive of', response['owner']['user']['displayName'] + ' (',
              response['driveType'] + ' ).',
              '\nConnection valid for one hour. Reauthenticate if required.')
    elif response.status_code == 401:
        response = json.loads(response.text)
        print('API Error! : ', response['error']['code'],
              '\nSee response for more details.')
    else:
        response = json.loads(response.text)
        print('Unknown error! See response for more details.')
    resp = make_response("One Drive \
                        successfully authenticationed, \
                        hit the back arrow twice to return to main menu")
    json_headers = json.dumps(headers, indent=4)
    resp.set_cookie(session["username"], json_headers)  # setting the session ID
    return resp


def check_for_duplicate_group(group_name):
    """Check for the existence of a group with the given name in the database.

    This function connects to the 'group.db' SQLite database and executes a query to select
    a group with the provided group_name from the 'groups' table. If a group with the given
    name exists, it returns the group; otherwise, it returns None.

    Parameters:
    group_name (str): The name of the group to check for duplicates.

    Returns:
    object: The existing group if found, None otherwise.
    """

    connection = sqlite3.connect("group.db")
    cursor = connection.cursor()
    cursor.execute("SELECT group_name FROM groups WHERE group_name = ?", (group_name,))
    existing_group = cursor.fetchone()
    connection.close()
    return existing_group is not None


@app.route("/create_group", methods=["POST"])
def create_group():
    """Summary: Creates a seperate folder with the title of the group in onedrive.
    Params:
    Returns:
    """
    group_name = request.form.get("group_name")

    # Retrieve authentication headers
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])

    if json_headers is None:
        return jsonify({"error": "Authentication headers not found"}), 401

    headers = json.loads(json_headers)
    # if "value" not in headers:
    #    return onedrive()

    # Create folder in OneDrive
    create_url = url + "/me/drive/root/children"
    body = {
        "name": "NotesApp-" + group_name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename",
    }

    try:
        response = requests.post(create_url, headers=headers, json=body, timeout=30)
        response.raise_for_status()  # Raise an error for non-2xx status codes
        return (
            render_template("groups.html", message="Folder created successfully"),
            200,
        )
    except requests.exceptions.RequestException as e:
        return (
            render_template(
                "groups.html",
                error=f"Failed to create group folder in OneDrive: {str(e)}",
            ),
            500,
        )


@app.route("/get_main_folders")
def get_main_folders():
    """Summary: Gets the shared and personal folders, displays them.
    Params:
    Returns:
    """
    shared_folder = File(None, "Shared With Me", None, None)
    shared_folder.set_filetype()
    shared_folder.set_file_icon()
    my_folder = File(None, "My Files", None, None)
    my_folder.set_filetype()
    my_folder.set_file_icon()

    return render_template(
        "main_folder.html", shared_folder=shared_folder, my_folder=my_folder
    )


@app.route("/get_shared_folders")
def get_shared_folders():
    """Function that lists the files in a User's onedrive.
    Parameters:
    None.
    Returns:
    flask method with the filexplorer.html page with the OneDrive files.
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    """
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return onedrive()
    headers = json.loads(json_headers)
    file_list = []
    timeout = 30
    items = json.loads(
        requests.get(
            url + "/me/drive/sharedWithMe", headers=headers, timeout=timeout
        ).text
    )
    if 'value' not in items:
        return onedrive()
    items = items["value"]
    #  for entries in range(len(items)):
    for _, entry in enumerate(items):
        # get folders
        remote_item = entry["remoteItem"]
        parent_ref = remote_item["parentReference"]
        id_linked = parent_ref["driveId"] + "," + remote_item["id"]
        new_file = File(id_linked, entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        if "folder" in new_file.get_filetype() and 'NotesApp-' in entry["name"]:
            file_list.append(new_file)
    return render_template("shared_file_groups.html", folders=file_list)


@app.route("/get_my_folders")
def get_my_folders():
    """Function that lists the files in a User's onedrive.
    Parameters:
    None.
    Returns:
    flask method with the filexplorer.html page with the OneDrive files.
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    """
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return onedrive()
    headers = json.loads(json_headers)
    file_list = []
    timeout = 30
    items = json.loads(
        requests.get(
            url + "me/drive/root/children", headers=headers, timeout=timeout
        ).text
    )
    if 'value' not in items:
        return onedrive()
    items = items["value"]
    #  for entries in range(len(items)):
    for _, entry in enumerate(items):
        # get folders
        new_file = File(entry["id"], entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        if "folder" in new_file.get_filetype() and 'NotesApp-' in entry['name'] \
                and "NotesApp-Favorites" not in entry['name']:
            file_list.append(new_file)
    return render_template("file_groups.html", folders=file_list)


@app.route("/get_my_personal_files", methods=["POST"])
def get_my_personal_files():
    """Summary
    Params:
    Returns:
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    url = "https://graph.microsoft.com/v1.0/"
    current_folder = request.form["file_id"]
    new_url = url + "me/drive/items/" + current_folder + "/children"
    sub_items = json.loads(requests.get(new_url, headers=headers, timeout=timeout).text)
    sub_items = sub_items["value"]
    for _, sub_entry in enumerate(sub_items):
        new_file = File(sub_entry["id"], sub_entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        file_list.append(new_file)
    return render_template("fileexplorer.html", folders=file_list)


@app.route("/get_my_shared_files", methods=["POST"])
def get_my_shared_files():
    """Summary
    Params:
    Returns:
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    Sources: Looked at: https://learn.microsoft.com/en-us/onedrive/developer/
    rest-api/api/driveitem_createlink?view=odsp-graph-online
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    url = "https://graph.microsoft.com/v1.0/"
    current_folder_ids = request.form["file_id"]
    ids_split = current_folder_ids.split(",")
    drive_id = ids_split[0]
    remote_id = ids_split[1]
    new_url = url + "drives/" + drive_id + "/items/" + remote_id + "/children"
    sub_items = json.loads(requests.get(new_url, headers=headers, timeout=timeout).text)
    sub_items = sub_items["value"]
    for _, sub_entry in enumerate(sub_items):
        id_field = sub_entry["id"] + "," + drive_id
        new_file = File(id_field, sub_entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        file_list.append(new_file)
    return render_template("fileexplorer_shared.html", folders=file_list)


@app.route("/delete_file", methods=["POST"])
@login_required
def delete_file():
    """Summary:
    Params:
    Returns:
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_id = request.form["file_id"]
    file_name = request.form["file_title"]
    m_url = "https://graph.microsoft.com/v1.0/"
    url = "/me/drive/items/" + file_id
    url = m_url + url
    response = requests.delete(url, headers=headers, timeout=timeout)
    if response.status_code == 204:
        message = "Item gone! If need to recover, please check OneDrive Recycle Bin."
    else:
        message = "Item could not be deleted. Go back and try again"
        return onedrive()
    return render_template("deleted_file.html", title=file_name, message=message)


@app.route("/download_file", methods=["POST"])
@login_required
def download_file():
    """Summary: Downloading files from One Drive
    Params:
    Returns:
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    m_url = "https://graph.microsoft.com/v1.0/"
    file_id = request.form["file_id"]
    file_title = request.form["file_title"]
    url = "me/drive/items/" + file_id + "/content"
    url = m_url + url
    file_name = file_title
    response_file_content = requests.get(url, headers=headers, timeout=timeout)
    if response_file_content.status_code != 200:
        return onedrive()
    return send_file(
        io.BytesIO(response_file_content.content),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=file_name
    )


@app.route("/download_file_shared", methods=["POST"])
@login_required
def download_file_shared():
    """Summary: Downloading files from One Drive
    Params:
    Returns:
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    Sources: Also used: https://learn.microsoft.com/en-us/onedrive/developer/
    rest-api/api/driveitem_createlink?view=odsp-graph-online
    """
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    m_url = "https://graph.microsoft.com/v1.0/"
    file_id = request.form["file_id"]
    file_id = file_id.split(',')[0]
    file_title = request.form["file_title"]
    url = "me/drive/items/" + file_id + "/content"
    url = m_url + url
    file_name = file_title
    response_file_content = requests.get(url, headers=headers, timeout=timeout)
    return send_file(
        io.BytesIO(response_file_content.content),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=file_name
    )


@app.route("/get_favorites", methods=["GET", "POST"])
def get_favorites():
    '''this function helps to display files in fav_tab'''
    timeout = 30
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    url = "https://graph.microsoft.com/v1.0/"
    current_folder = get_or_create_favorites_folder(headers)
    if current_folder is None:
        return onedrive()
    new_url = url + "me/drive/items/" + current_folder + "/children"
    sub_items = json.loads(requests.get(new_url, headers=headers, timeout=timeout).text)
    if "value" not in sub_items:
        return onedrive()
    sub_items = sub_items["value"]
    for _, sub_entry in enumerate(sub_items):
        new_file = File(sub_entry["id"], sub_entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        file_list.append(new_file)
    return render_template("favoriteexplorer.html", folders=file_list)


@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    """ move file to favorites folder
    """
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_id = request.form["file_id"]
    m_url = "https://graph.microsoft.com/v1.0/"
    url = "/me/drive/items/" + file_id
    url = m_url + url
    favorites_folder_id = get_or_create_favorites_folder(headers)
    copy_file_to_favorites(headers, file_id, favorites_folder_id)
    return get_favorites()


@app.route("/add_favorite_shared", methods=["POST"])
def add_favorite_shared():
    """ move file to favorites folder from shared folder
    """
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_id = request.form["file_id"]
    m_url = "https://graph.microsoft.com/v1.0/"
    url = "/me/drive/items/" + file_id
    url = m_url + url
    favorites_folder_id = get_or_create_favorites_folder(headers)
    copy_file_to_favorites_shared(headers, file_id, favorites_folder_id)
    return get_favorites()


def get_or_create_favorites_folder(headers):
    '''Summary:'''
    search_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    response = requests.get(search_url, headers=headers, timeout=30)
    if response.status_code == 200:
        folders = response.json()['value']
        for folder in folders:
            if folder.get('name') == 'NotesApp-Favorites' and 'folder' in folder:
                return folder['id']
        create_folder_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
        payload = {
            "name": "NotesApp-Favorites",
            "folder": {}
        }
        share_response = requests.post(create_folder_url, headers=headers, json=payload, timeout=30)
        get_or_create_favorites_folder(headers)

        if share_response == 400:
            print("error")
            return onedrive()
    return None


@app.route("/searchfiles", methods=["POST"])
@login_required
def searchfiles():
    """Summary: Search Files
    Params:
    Returns:
    Links: Adapted from: "list folder under directory method"
    https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python"""
    search_criteria = request.form["Search"]
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    file_list = []
    timeout = 30
    items = json.loads(
        requests.get(
            url + "me/drive/root/children", headers=headers, timeout=timeout
        ).text
    )
    if 'value' not in items:
        return onedrive()
    items = items["value"]
    for _, entry in enumerate(items):
        new_file = File(entry["id"], entry["name"], None, None)
        new_file.set_filetype()
        new_file.set_file_icon()
        if "NotesApp-" in entry["name"] and "NotesApp-Favorites" not in entry["name"]:
            current_folder = entry["id"]
            new_url = url + "me/drive/items/" + current_folder + "/children"
            sub_items = json.loads(
                requests.get(new_url, headers=headers, timeout=timeout).text
            )
            sub_items = sub_items["value"]
            for _, sub_entry in enumerate(sub_items):
                new_file = File(sub_entry["id"], sub_entry["name"], None, None)
                new_file.set_filetype()
                new_file.set_file_icon()
                if search_criteria.lower() in sub_entry["name"]:
                    file_list.append(new_file)
    return render_template("searchtemplate.html", folders=file_list)


@app.route("/share_my_group", methods=["POST"])
@login_required
def share_group_setup():
    """Sumary: sets up for sharing personal file"""
    file_id = request.form["file_id"]
    title = request.form["title"]
    return render_template("share_group_setup.html", file_id=file_id, title=title)


@app.route("/share_group_action", methods=["POST"])
@login_required
def share_group_action():
    """Summary: Share personal group with someone
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    """
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    email = request.form["email"]
    folder_id = request.form["file_id"]
    title = request.form["title"]
    share_data = {
        "recipients": [{"email": email}],
        "requireSignIn": True,
        "sendInvitation": True,
        "roles": ["write"],
    }
    share_response = requests.post(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/invite",
        headers=headers,
        json=share_data,
        timeout=30,
    )
    if share_response == 400:
        print("error")
        return onedrive()
    return render_template("share_group_setup.html", file_id=folder_id, title=title)


@app.route("/share_my_group_shared", methods=["POST"])
@login_required
def share_group_setup_shared():
    """Sumary: sets up for sharing shared group"""
    file_id = request.form["file_id"]
    title = request.form["title"]
    return render_template(
        "shared_group_setup_shared.html", file_id=file_id, title=title
    )


@app.route("/share_group_action_shared", methods=["POST"])
@login_required
def share_group_action_shared():
    """Summary: Share shared group with someone
    Sources: Adapted from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
    """
    timeout = 60
    url = "https://graph.microsoft.com/v1.0/"
    json_headers = request.cookies.get(session["username"])
    if json_headers is None:
        return render_template("homepage.html")
    headers = json.loads(json_headers)
    email = request.form["email"]
    folder_id = request.form["file_id"]
    current_folder_ids = request.form["file_id"]
    ids_split = current_folder_ids.split(",")
    drive_id = ids_split[0]
    remote_id = ids_split[1]
    new_url = url + "drives/" + drive_id + "/items/" + remote_id + "/invite"
    title = request.form["title"]
    share_data = {
        "recipients": [{"email": email}],
        "requireSignIn": True,
        "sendInvitation": True,
        "roles": ["write"],
    }
    share_response = requests.post(
        new_url, headers=headers, json=share_data, timeout=timeout
    )
    if share_response == 400:
        print("error")
        return onedrive()
    return render_template(
        "shared_group_setup_shared.html", file_id=folder_id, title=title
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
    checkdatabase()
    login()
