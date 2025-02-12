import hashlib
import sys

from . import web


def hash_bytes(bytes_object: bytes, hash_algo: str):
    # Equivalent to sha256 example: hashlib.sha256(bytes_object).hexdigest()
    return getattr(hashlib, hash_algo)(bytes_object).hexdigest()


def hash_url(url: str, hash_algo: str, user_agent: str = str(), default_user_agent: bool = True):
    response = web.get_page_bytes(url, user_agent=user_agent, default_user_agent=default_user_agent)
    return hash_bytes(response, hash_algo)


def hash_file(file_path: str, hash_algo: str, block_size: int = 1024):
    """
    The function will return hash of the file with specified algorithm.

    :param file_path: string, full file path to file to hash.
    :param hash_algo: string, file hashing algorithm. Tested:
        md5, sha256, sha1
    :param block_size: integer, of block size in bytes that will be hashed at a time.
    """

    # Function from python 3.8 and above because of 'assignment expression'.
    if (3, 8) <= sys.version_info < (3, 11):
        # Example for type specific: hashlib.sha256()
        hashlib_object = getattr(hashlib, hash_algo)()
        bytearray_empty = bytearray(128*block_size)
        memoryview_object = memoryview(bytearray_empty)
        with open(file_path, 'rb', buffering=0) as file_object:
            # noinspection PyUnresolvedReferences
            while n := file_object.readinto(memoryview_object):
                hashlib_object.update(memoryview_object[:n])
        return hashlib_object.hexdigest()
    # From python version 3.11 there is new easier function for that.
    elif sys.version_info >= (3, 11):
        with open(file_path, 'rb', buffering=0) as file_object:
            return hashlib.file_digest(file_object, hash_algo).hexdigest()
