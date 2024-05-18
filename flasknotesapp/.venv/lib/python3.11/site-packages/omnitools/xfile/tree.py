from .path import join_path
import os


def format_cascade(r, key=0, sep=os.path.sep, f_sep=" "):
    for _ in r:
        if not _[-1].startswith(sep):
            if sep == "\\":
                if _[-1][1:3] != ":\\":
                    _[-1] = sep+_[-1]
            else:
                _[-1] = sep+_[-1]
    tuple_len = len(r[0])-1
    r.sort(key=lambda x: x[key])
    root = os.path.join(r[0][key], sep)
    mapped = {}
    seen = set()
    for _ in r:
        k = _.pop(key)
        mapped[k] = _
    def get_children(root):
        children = []
        children_seen = set()
        for _, v in mapped.items():
            if _ in seen:
                continue
            if _.startswith(root):
                rest = _[len(root):].split(sep)
                child = root+rest[0]+(sep if len(rest)>1 else "")
                if child in children_seen:
                    continue
                if _ == child:
                    children.append([child, v])
                    seen.add(_)
                else:
                    children.append([child, [""]*tuple_len])
                children_seen.add(child)
        return sorted(children, key=lambda x: x[0])
    # return print(get_children(root))
    targets = [root]
    text = [[root, [""]*tuple_len]]
    index = {}
    while True:
        if not targets:
            break
        t = targets.pop(0)
        # print("\r", t, len(r), end="", flush=True)
        c = get_children(t)
        c.sort(key=lambda x: [0 if x[0].endswith(sep) else 1, x])
        if text == [[root, [""]*tuple_len]]:
            pindex = 0
            for i in range(0, len(c)):
                text.append(["{}---- {}".format(
                    "'" if i == len(c)-1 else "|",
                    c[i][0].split(sep)[-2 if c[i][0].endswith(sep) else -1]
                ), c[i][1]])
                index[c[i][0]] = pindex+1
                pindex += 1
        else:
            pindex = None
            for i in range(0, len(c)):
                text.insert(index[t]+1 if pindex is None else pindex+1, ["{}{}---- {}".format(
                    "|   "*(t.count(sep)-1),
                    "'" if i == len(c)-1 else "|",
                    c[i][0].split(sep)[-2 if c[i][0].endswith(sep) else -1]
                ), c[i][1]])
                if pindex is None:
                    for k, v in index.items():
                        if v >= index[t]+1:
                            index[k] += 1
                    index[c[i][0]] = index[t]+1
                    pindex = index[t]+1
                else:
                    for k, v in index.items():
                        if v >= pindex+1:
                            index[k] += 1
                    index[c[i][0]] = pindex+1
                    pindex += 1
        cc = [_[0] for _ in c if _[0].endswith(sep)]
        # if not cc:
        #     print("\r\t", t, len(c))
        # if t == "/X/TD/collection/[魔穗字幕组]/Incomplete/2017/[魔穗字幕组]2017年4月作品合集/":
        #     print("\r\t", t, len(c))
        #     print(c)
        targets = cc+targets
        # print(t, c)
        # input()
        # print("\t", c)
        # print(index)
    # print("\n".join(["\t".join([_[0], *_[1]]) for _ in text]))
    for i, _ in enumerate(text):
        try:
            ind = _[0].index("'")
            # print(_, ind)
            pj = None
            for j in range(i+1, len(text)):
                if pj is not None and j-pj!=1:
                    # print(j, pj)
                    break
                __ = text[j]
                if __[0][ind] == "|":
                    if pj is None or j-pj==1:
                        text[j][0] = __[0][:ind]+" "+__[0][ind+1:]
                        pj = j
                if pj is None and j == i+1:
                    break
        except:
            continue
    # [print(_) for _ in text]
    # print([_ for _ in text if len(_)!=2])
    cols = zip(*list(mapped.values()))
    max_len = [len(max(_, key=len)) for _ in cols]
    template = ""
    for _ in max_len:
        if template:
            template += f_sep
        template += "{{:>{}}}".format(_)
    return "\n".join(["{}{}{}".format(
        template.format(*v),
        f_sep,
        _,
    ) for _, v in text])


