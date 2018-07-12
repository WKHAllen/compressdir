"""Compress and decompress files and directories.

Example:
    >>> from compressdir import compress
    >>> path = "/path/to/file/or/dir"
    >>> compress(path)
    >>> decompress(path + ".compressed")
"""

import os
import bz2
try:
    import cPickle as pickle
except ImportError:
    import pickle
from easyencrypt import symmetricEncrypt, symmetricDecrypt, passwordToKey

def compressed(path, encryptKey=None, maximumCompression=False):
    """Compress a file or directory."""
    def splitPath(path):
        pathsplit = []
        while True:
            path, part = os.path.split(path)
            if part != "":
                pathsplit.append(part)
            else:
                if path != "":
                    pathsplit.append(path)
                pathsplit.reverse()
                return pathsplit

    def dirToDict(path):
        pathlist = []
        for root, dirs, files in os.walk(path):
            for d in dirs:
                pathlist.append(os.path.join(root, d))
            for f in files:
                pathlist.append(os.path.join(root, f))
        tree = {}
        for thepath in pathlist:
            p = tree
            parts = splitPath(thepath)
            for part in parts:
                p = p.setdefault(part, {})
        for _ in range(len(splitPath(path)) - 1):
            tree = tree[list(tree.keys())[0]]
        return tree

    def fileData(path, tree):
        for key in list(tree.keys()):
            if os.path.isdir(os.path.join(path, key)):
                tree[key] = fileData(os.path.join(path, key), tree[key])
            else:
                try:
                    with open(os.path.join(path, key), "r") as f:
                        tree[key] = f.read()
                except:
                    with open(os.path.join(path, key), "rb") as f:
                        tree[key] = f.read()
        return tree

    if os.path.isdir(path):
        tree = dirToDict(path)
        data = {list(tree.keys())[0]: fileData(path, list(tree.values())[0])}
    else:
        try:
            with open(path, "r") as f:
                data = {os.path.split(path)[1]: f.read()}
        except:
            with open(path, "rb") as f:
                data = {os.path.split(path)[1]: f.read()}

    pickled = pickle.dumps(data)
    if maximumCompression:
        data = bz2.compress(pickled)
        for i in range(1, 10):
            newdata = bz2.compress(pickled, compresslevel=i)
            if len(newdata) < len(data):
                data = newdata
    else:
        data = bz2.compress(pickled, compresslevel=9)

    if encryptKey is not None:
        try:
            data = symmetricEncrypt(data, encryptKey)
        except:
            data = symmetricEncrypt(data, passwordToKey(encryptKey))

    return data

def compress(path, newpath=None, encryptKey=None, maximumCompression=False, ext=".compressed"):
    """Compress a file or directory and write it to a file."""
    data = compressed(path, encryptKey=encryptKey, maximumCompression=maximumCompression)

    if newpath is None:
        newpath = os.path.join(os.path.split(path)[0], os.path.splitext(os.path.split(path)[1])[0] + ext)

    open(newpath, "wb").close()
    with open(newpath, "wb") as f:
        f.write(data)

def decompressed(data, newpath, decryptKey=None):
    """Decompress a byte string compression of a file or directory."""
    def dictToDir(path, tree):
        for key in list(tree.keys()):
            if type(tree[key]) is type(str()):
                with open(os.path.join(path, key), "w") as f:
                    f.write(tree[key])
            elif type(tree[key]) is type(bytes()):
                with open(os.path.join(path, key), "wb") as f:
                    f.write(tree[key])
            elif type(tree[key]) is type(dict()):
                if not os.path.exists(os.path.join(path, key)):
                    os.mkdir(os.path.join(path, key))
                dictToDir(os.path.join(path, key), tree[key])

    if decryptKey is not None:
        try:
            data = symmetricDecrypt(data, decryptKey)
        except:
            data = symmetricDecrypt(data, passwordToKey(decryptKey))
    data = bz2.decompress(data)
    data = pickle.loads(data)
    dictToDir(newpath, data)

def decompress(path, newpath=None, decryptKey=None):
    """Decompress a file or directory."""
    if newpath is None:
        newpath = os.path.split(path)[0]

    with open(path, "rb") as f:
        data = f.read()
    decompressed(data, newpath, decryptKey=decryptKey)
