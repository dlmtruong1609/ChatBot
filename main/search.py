from googlesearch import search
import webbrowser

class Search():
    def search(text):
        for url in search(text, stop=1):
            a_website = url
        print(url)
        # Open url in a new window of the default browser, if possible
        webbrowser.open_new(a_website)

