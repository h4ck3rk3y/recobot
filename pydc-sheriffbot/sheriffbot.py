import copy, datetime, os, sys, timefrom pydc_client import pydc_clientfrom pymongo import MongoClientfrom xml.dom.minidom import parseimport xml.dom.minidomfrom pprint import pprintimport mimetypessupported_file_types = ['mkv','mp4', 'avi']client = MongoClient("mongodb://localhost:27017")db = client.reco_bot_2tths = db.tthsuser_list = db.user_listdone_users = db.done_usersdef crank(data):	if "+reco" in data:		nick = re.findall("^<(.*)>",data)		c.pm_send(nick,get_reco(nick).join("\n"))data = { "mode":True, "name":"pyDC", "host":"172.17.26.89","nick":"monkey_see_monkey_do","pass":"banana","desc":"filelist_dede","email":"","sharesize":10995116277760,"localhost":"172.17.30.135"}c = pydc_client().configure(data).link({"mainchat":crank,"debug":[sys.stdout.write,open("debug.txt","w").write,None][2] }).connect("0/1/0");c._config["overwrite"] = Truetime.sleep(3); # Wait for the connection to established and session to be verified.def filelist_analyse(filename,nick):    print "Filelist download complete :", nick, filename[:-4]    DOMTree = xml.dom.minidom.parse(filename[:-4])    for file_ob in (DOMTree.getElementsByTagName('File')):        file_name =  file_ob.attributes['Name'].value        tth =  file_ob.attributes['TTH'].value        size =  file_ob.attributes['Size'].value        if int(size) < 104857600:        	continue        for x in supported_file_types:            if  file_name.endswith(x):                f = tths.find({'tth': tth})                user_list.insert({'tth': tth, 'creation_date': datetime.datetime.now(), 'user': unicode(nick, errors='replace') })                if f.count() ==0:                    tths.insert({'tth': tth, 'name': file_name.encode('utf-8')})                break    done_users.insert({'user': unicode(nick, errors='replace')})if __name__=="__main__":    while True:        c._nicklock.acquire()        nicklist = copy.deepcopy(c._nicklist)        c._nicklock.release()        number_of_users = len(nicklist)        print number_of_users        for nick in nicklist:            already_processed = done_users.find({'user': unicode(nick, errors='replace')})            if not nicklist[nick]["operator"] and not nicklist[nick]["bot"] and already_processed.count()==0:            	user_list.remove({'user': unicode(nick, errors='replace')})                c.download_filelist(nick,filelist_analyse,nick)        break    c.cli()"""To share files, manually add them using ~self.filelist_add(<path>) and ~self.filelist_generate()"""