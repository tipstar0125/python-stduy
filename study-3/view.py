import eel
import desktop
import search

app_name="html"
end_point="index.html"
size=(700,600)

@ eel.expose
def kimetsu_search(search_keyword, source_file):
    search_result = search.kimetsu_search(search_keyword, source_file)
    # print(search_result)
    eel.view_log_js(search_result)

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)
