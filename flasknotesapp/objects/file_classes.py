""" Module containing methods related to files"""

import re


class File:
    """A class representing a File.

    A file has a unique identifier, a title, a list of tags,
    and a list of entities with whom the file is shared.
    """
    file_id: int
    title: str
    tags: list[str]
    shared_with: list[int]

    # Assuming shared_with is a list of UserIDs or GroupIDs for simplicity

    def __init__(self, file_id: int, title: str, filetype: str,
                 fileicon: str):
        self.file_id = file_id
        self.title = title
        self.filetype = filetype
        self.fileicon = fileicon

    def get_file_id(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return self.file_id

    def get_title(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return self.title

    def set_filetype(self):
        '''Summary: Sets the filetype from the file name

        Paramters:

        Returns: Nothing, sets the filetype to the filetype
        '''
        if '.' not in self.title:
            self.filetype = ['folder']
        else:
            filetype = re.findall(r'[.][a-zA-Z]{1,4}', self.title)
            self.filetype = filetype

    def get_filetype(self):
        '''Summary: returns the filetype

        Paramters:

        Returns:
        '''
        return str(self.filetype)

    def set_file_icon(self):
        '''Summary: Sets the file icon to the correct icon, the correct file image address

        Paramters:

        Returns:
        '''
        file_icons = {
            '.docx': "static/file_icons/docx_file_icon.png",
            '.jpg': "static/file_icons/jpeg_icon.png",
            '.pdf': "static/file_icons/pdf_icon.png",
            'folder': "static/file_icons/folder_icon.png",
            '.sas': "static/file_icons/sas_icon.png",
            '.csv': "static/file_icons/csv_icon.png",
            '.obj': "static/file_icons/obj_icon.png",
            '.R': "static/file_icons/r_icon.png",
            '.py': "static/file_icons/py_icon.svg",
            '.png': "static/file_icons/png_icon.png",
            '.tex': "static/file_icons/tex_icon.png",
            '.xlsx': "static/file_icons/xlsx_icon.png"
            }
        # Set the file icon based on the file extension
        self.fileicon = file_icons.get(self.filetype[0], "static/file_icons/default_icon.png")
