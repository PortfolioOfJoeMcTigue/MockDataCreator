import webbrowser


class ServiceOperations():

  def open_html_file_in_chrome(self):
      print("   inside: open_html_file_in_chrome")
      webbrowser.get("C://Program Files (x86)//Google//Chrome//Application//chrome.exe %s &").open("file://C:/Users/josep/Projects/Python/Mock-Data-Creator/documentation/help.html")
      print("   leaving: open_html_file_in_chrome")