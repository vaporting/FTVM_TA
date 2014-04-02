import sys

class Preprocess_Error(Exception):
  def __init__(self, content):
    self.content = content
  def __str__(self):
    return content

class Process_Error(Exception):
  def __init__(self, content):
    self.content = content
  def __str__(self):
    return content

class Assert_Error(Exception):
  def __init__(self, content):
    self.content = content
  def __str__(self):
    return content

class Postprocess_Error(Exception):
  def __init__(self, content):
    self.content = content
  def __str__(self):
    return content


class Shell_server_Error(Exception):
  def __init__(self, content):
    self.content = content
  def __str__(self):
    return content
