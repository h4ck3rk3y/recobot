import copy, datetime, os, sys, timefrom dc_client.pydc_client import *from pymongo import MongoClientfrom xml.dom.minidom import parseimport xml.dom.minidomfrom pprint import pprintimport mimetypesimport build_matriximport recomimport reimport unidecodesupported_file_types = ['mkv','mp4', 'avi']client = MongoClient("mongodb://localhost:27017")db = client.reco_bot_2tths = db.tthsuser_list = db.user_listdone_users = db.done_usersflag = Falsedef recommend(text):    try:        if not type(text) is str:            text = unidecode.unidecode(text)        nick = re.findall("^<(.*)>",text)        if nick is None or len(nick) == 0 or nick[0] == '\x95Security\x95':            return        if flag == False and '+reco' in text:            print nick            c.pm_send(nick, 'bot is loading....')            return        nick = nick[0]        count = db.done_users.count({'user': nick, 'recommended':True})        if count == 0 and '+reco' in text:            c.pm_send(nick, 'sorry your data is not in the database, your recommendation may take some time')            count = db.done_users.count({'user': nick})            if count == 0 and "+reco users" in text:                c.download_filelist(nick,filelist_analyse,{'nick':nick, 'command': 'users'})            elif count == 0:                c.download_filelist(nick,filelist_analyse,{'nick':nick, 'command': 'files'})            elif "+reco users" in text:                c.pm_send(nick,"\n"+"\n".join(recom.similar_users(nick)[1:]))                c.pm_send(nick, "all hail lord cranky and lord pohemia")            elif "+reco" in text:                c.pm_send(nick, "\n"+"\n".join(recom.recommended_files(nick)))                c.pm_send(nick, "all hail lord cranky and lord pohemia")        elif "+reco users" in text:            c.pm_send(nick,"\n"+"\n".join(recom.similar_users(nick)[1:]))            c.pm_send(nick, "all hail lord cranky and lord pohemia")        elif "+reco" in text:            c.pm_send(nick, "\n"+"\n".join(recom.recommended_files(nick)))            c.pm_send(nick, "all hail lord cranky and lord pohemia")    except:        passconfig_data = { "mode":True, "name":"reco_reco_reco", "host":"172.17.26.89","nick":"recobot","pass":"banana","desc":"filelist_dede","email":"","sharesize":10995116277760,"localhost":"172.17.30.135"}c = pydc_client().configure(config_data).link({"mainchat":recommend,"debug":[sys.stdout.write,open("debug.txt","w").write,None][2] }).connect("0/1/0");c._config["overwrite"] = Truetime.sleep(3); # Wait for the connection to established and session to be verified.def filelist_analyse(filename,blob):    nick = blob['nick']    if not type(nick) is str:        nick = unidecode.unidecode(nick)    print "Filelist download complete :", nick, filename[:-4]    DOMTree = xml.dom.minidom.parse(filename[:-4])    file_exists = False    for file_ob in (DOMTree.getElementsByTagName('File')):        file_name =  file_ob.attributes['Name'].value        tth =  file_ob.attributes['TTH'].value        size =  file_ob.attributes['Size'].value        if int(size) < 104857600:            continue        for x in supported_file_types:            if  file_name.endswith(x):                f = tths.find({'tth': tth})                user_list.insert({'tth': tth, 'creation_date': datetime.datetime.now(), 'user': nick })                file_exists = True                if f.count() ==0:                    tths.insert({'tth': tth, 'name': file_name.encode('utf-8')})                break    if file_exists:        done_users.insert({'user': nick, 'recommended': False})        if blob.has_key('command'):            if blob['command'] == 'users':                c.pm_send(nick,"\n"+"\n".join(recom.similar_users(nick)[1:]))                c.pm_send(nick, "all hail lord cranky and lord pohemia")            elif blob['command'] == 'files':                c.pm_send(nick, "\n"+"\n".join(recom.recommended_files(nick)))                c.pm_send(nick, "all hail lord cranky and lord pohemia")    elif blob.has_key('command'):        c.pm_send(nick, 'no supported file above 100 MB found in your file list :/. share more?')        c.pm_send(nick, "all hail lord cranky and lord pohemia")if __name__=="__main__":    c.mc_send('recobot is ONLINE, building database')    get_file_lists = raw_input("Download Filelists?\n$>")    if get_file_lists.lower() == 'y':        print 'downloading filelists .. this will take some time'        while True:            c._nicklock.acquire()            nicklist = copy.deepcopy(c._nicklist)            c._nicklock.release()            number_of_users = len(nicklist)            print number_of_users            for nick in nicklist:                if not type(nick) is str:                    nick = unidecode.unidecode(nick)                already_processed = done_users.find({'user': nick})                if not nicklist[nick]["operator"] and not nicklist[nick]["bot"] and already_processed.count()==0:                    user_list.remove({'user': nick})                    c.download_filelist(nick,filelist_analyse,{'nick': nick})            break    rebuild_recommendations = raw_input('Press y to rebuild recomendation database\n$>')    if rebuild_recommendations.lower() == 'y':        print 'bot is building matrix'        build_matrix.dat_build()    flag = True    c.mc_send('reco bot is online try +reco or +reco users')    c.mc_send("\t".join(supported_file_types) + "\tare the supported_file_types")    c.cli()