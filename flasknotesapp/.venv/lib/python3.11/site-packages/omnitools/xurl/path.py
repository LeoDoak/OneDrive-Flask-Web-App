# import requests
# from lxml import html
#
#
# def rlookup(path):
#     if not path.endswith("/"):
#         path = "/".join(path.split("/")[:-1])
#         if len(path) > 0:
#             path += "/"
#     r = s.get(domain+path).content.decode()
#     r = html.fromstring(r)
#     hrefs = r.xpath("//a/@href")
#     for href in hrefs:
#         if href.find("://") != -1:
#             url = domain+path
#         elif href.startswith("//"):
#             url = domain[6:]+path
#         else:
#             url = ""
#         if href.startswith("#") or href.startswith("/") or href == url or href.find("..") >= 0:
#             continue
#         elif href.startswith(url):
#             # print(url, href, path)
#             if url != "":
#                 href = href.replace(domain+path, "")
#             if not href in paths:
#                 paths.append(path+href)
#             else:
#                 continue
#             if href.endswith("/") and not "." in href:
#                 print(path+href)
#                 rlookup(path+href)
#
#
# # txt = open(r"D:\foxe6\imooc.txt", "rb").read().splitlines()
# # results = ""
# # for line in txt:
# #     line = line.decode()
# #     if line.startswith("imooc"):
# #         results += "\n\n"+line + "\n"
# #     elif line.startswith("├"):
# #         results += line+"\n"
# # open(r"D:\foxe6\imooc.result.txt", "wb").write(results.encode())
# # exit()
# # txt = open(r"D:\foxe6\mooc.txt", "rb").read().splitlines()
# # import re
# # results = ""
# # rule = rb"(python|web|html|css|javascipt|js|jquery|vue|react|angular)"
# # for i, line in enumerate(txt):
# #     if b"'py': 'python'" in line:
# #         continue
# #     result = re.search(rule, line.lower())
# #     if result is not None:
# #         try:
# #             a = html.fromstring(line.decode()).xpath("//*/text()")[0]
# #             b = html.fromstring(txt[i+1].decode()).xpath("//*/text()")[0]
# #             if not b.startswith("http"):
# #                 b = html.fromstring(txt[i+2].decode()).xpath("//*/text()")[0]
# #             if not b.startswith("http"):
# #                 b = html.fromstring(txt[i+3].decode()).xpath("//*/text()")[0]
# #             if not b.startswith("http"):
# #                 continue
# #             results += b.ljust(80)+a+"\n"
# #         except:
# #             pass
# # open(r"D:\foxe6\mooc.result.txt", "wb").write(results.encode())
# # exit()
# # domain = "https://archive.rhilip.info/"
# domain = "https://archive.org/"
# s = requests.Session()
# s.headers.update({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
# paths = []
# # rlookup("index.md")
# # rlookup("学习资料/MOOC公开课程/")
# rlookup("download/footest2/a")
# files = [path for path in paths if not path.endswith("/")]
# print(files)
# # txt = ""
# # for file in files:
# #     r = s.get(domain+file).content.decode()
# #     txt += r+"\n"
# # open(r"D:\foxe6\test.txt", "wb").write(txt.encode())
