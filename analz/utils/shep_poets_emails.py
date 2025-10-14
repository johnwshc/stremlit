from pydantic import BaseModel


poets = """
Suzanne <cardedartist@gmail.com>,
Edward Zahniser <eddzahniser@comcast.net>,
Stephen Altman <stephen.altman@gmail.com>,
Hope Snyder <hms@hbp.com>,
bluecollar jedi <bluecollar_jedi@yahoo.com>,
Janet Harrison <jmrharrison@gmail.com>,
John Case <jcase4218@gmail.com>,
"tseffers@mail.com" <tseffers@mail.com>,
"calvinsmith99993@yahoo.com" <calvinsmith99993@yahoo.com>,
"foxfire0002@hotmail.com" <foxfire0002@hotmail.com>,
stanley niamatali <stanley.niamatali@gmail.com>,
"JPATE@shepherd.edu" <JPATE@shepherd.edu>,
"suesilver194@gmail.com" <suesilver194@gmail.com>,
"sf15561@gmail.com" <sf15561@gmail.com>,
"rylandswain@gmail.com" <rylandswain@gmail.com>,
Susan Hall-West <susanhw83@gmail.com>,
if <jstarjo@aol.com>,
"spatig@marshall.edu" <spatig@marshall.edu>,
Stewart Acuff <stewartacuff0180@gmail.com>,
"rlsibley@yahoo.com" <rlsibley@yahoo.com>,
"brwaldron69@yahoo.com" <brwaldron69@yahoo.com>,
"eldon@winstongardens.com" <eldon@winstongardens.com>,
"erundwd@yahoo.com" <erundwd@yahoo.com>,
"sshorrpa@shepherd.edu" <sshorrpa@shepherd.edu>,
"pastorjohnyost@comcast.net" <pastorjohnyost@comcast.net>,
"ricktaylor412@gmail.com" <ricktaylor412@gmail.com>,
"HelenHibbardBurns@gmail.com" <HelenHibbardBurns@gmail.com>,
Ginny Fite <gnnfite9@gmail.com>,
"richardstukey@msn.com" <richardstukey@msn.com>,
"jldeupree@gmail.com" <jldeupree@gmail.com>,
"sshurbut@shepherd.edu" <sshurbut@shepherd.edu>,
Arthur Stone LAST_NAME <jesse45@comcast.net>,
"themountainscribes@gmail.com" <themountainscribes@gmail.com>,
"chadua1@yahoo.com" <chadua1@yahoo.com>,
"write@hampshirearts.org" <write@hampshirearts.org>,
Lynn Swanson <blynswan@comcast.net>,
"john.e.berry3@gmail.com" <john.e.berry3@gmail.com>,
"peggyagordon@gmail.com" <peggyagordon@gmail.com>,
"janefreemanbooks@gmail.com" <janefreemanbooks@gmail.com>,
"director@theriverhousewv.org" <director@theriverhousewv.org>,
"eightorso@gmail.com" <eightorso@gmail.com>,
"grayshopcat@gmail.com" <grayshopcat@gmail.com>,
"scafidijr@yahoo.com" <scafidijr@yahoo.com>,
"m2davis@gmail.com" <m2davis@gmail.com>,
"4seasons114@gmail.com" <4seasons114@gmail.com>,
"artificerex9@gmail.com" <artificerex9@gmail.com>,
"illpass@comcast.net" <illpass@comcast.net>,
"alan@alanbgibson.com" <alan@alanbgibson.com>,
"ericquinn327@gmail.com" <ericquinn327@gmail.com>,
"ctlreads@ctlibrary.org" <ctlreads@ctlibrary.org>,
"BBANKHUR@shepherd.edu" <BBANKHUR@shepherd.edu>
"cath.irwin@comcast.net" <cath.irwin@comcast.net>,
"doug@mannamachine.com" <doug@mannamachine.com>,
"ramcquade@comcast.net" <ramcquade@comcast.net>,
"jeremyrboyd@gmail.com" <jeremyrboyd@gmail.com>,
"drsplaine@yahoo.com" <drsplaine@yahoo.com>,
"hlarew@gmail.com" <hlarew@gmail.com>,
"barbcupp@hotmail.com" <barbcupp@hotmail.com>,
"meredithcm2003@yahoo.com" <meredithcm2003@yahoo.com>,
"suzieq3535@comcast.net" <suzieq3535@comcast.net>,
"paulkradel@gmail.com" <paulkradel@gmail.com>,
"lauriepdx@outlook.com" <lauriepdx@outlook.com>,
"john.e.keeney@gmail.com" <john.e.keeney@gmail.com>,
"michellenfiles@gmail.com" <michellenfiles@gmail.com>,
"todd@flatrabbitmusic.com" <todd@flatrabbitmusic.com>,
"gdubose@gmail.com" <gdubose@gmail.com>,
"lwagner4@mac.com" <lwagner4@mac.com>,
"anvvbledsoe@gmail.com" <anvvbledsoe@gmail.com>,
"weldont67@aol.com" <weldont67@aol.com>,
"bethbatdorf@msn.com" <bethbatdorf@msn.com>,
"lwdoty@outlook.com" <lwdoty@outlook.com>,
"leigh@leighfleming.com" <leigh@leighfleming.com>,
"greenlisaa@icloud.com" <greenlisaa@icloud.com>,
"oliviarg629@gmail.com" <oliviarg629@gmail.com>,
"awhart02@rams.shepherd.edu" <awhart02@rams.shepherd.edu>,
"chapelb95@gmail.com" <chapelb95@gmail.com>,
"swilling1@frontier.com" <swilling1@frontier.com>,
"adugas317@gmail.com" <adugas317@gmail.com>,
"philipmscolaro@gmail.com" <philipmscolaro@gmail.com>,
"pericelik@yahoo.com" <pericelik@yahoo.com>,
"tommy195carlos@gmail.com" <tommy195carlos@gmail.com>,
"kathelinelauffer@hotmail.com" <kathelinelauffer@hotmail.com>,
"lara.d.elliott@gmail.com" <lara.d.elliott@gmail.com>,
"pflama01@rams.shepherd.edu" <pflama01@rams.shepherd.edu>,
"Solsburyhill.farm@yahoo.com" <Solsburyhill.farm@yahoo.com>,
"patadidonato@gmail.com" <patadidonato@gmail.com>,
"cbaldau@gmail.com" <cbaldau@gmail.com>,
"c_marujo@yahoo.com" <c_marujo@yahoo.com>,
"dreamcircle1111@gmail.com" <dreamcircle1111@gmail.com>,
"sean.r.murtagh@gmail.com" <sean.r.murtagh@gmail.com>,
"Chrissy.abruzzi@gmail.com" <Chrissy.abruzzi@gmail.com>,
"hhanraha@shepherd.edu" <hhanraha@shepherd.edu>,
"junger@shepherd.edu" <junger@shepherd.edu>,
"dale.leatherman@gmail.com" <dale.leatherman@gmail.com>,
"krobbi03@rams.shepherd.edu" <krobbi03@rams.shepherd.edu>,
"elle.alf222@gmail.com" <elle.alf222@gmail.com>,
"profkushin@gmail.com" <profkushin@gmail.com>,
"fisher4edits@gmail.com" <fisher4edits@gmail.com>,
"judywalter@pa.net" <judywalter@pa.net>,
"vstevens@shepherd.edu" <vstevens@shepherd.edu>"""


class Poet(BaseModel):
	name: str
	email: str

class BuildPoet():

	def __init__(self, d: dict):
		self.d = d

	def build_poet(self) -> Poet:
		return Poet(**self.d)


def get_poets():
	poets_list = poets.split("\n")
	poet_obj_list = []
	for poet in poets_list:
		if not poet: continue
		poet_dict = {}
		poet_l = poet.split(" ")
		poet_email = poet.split(" ")[-1]
		poet_email = poet_email.replace("<", "").replace(">", "")
		poet_name = ' '.join(poet_l[:-1])
		poet_dict['name'] = poet_name.replace("\"", "")
		poet_dict['email'] = poet_email
		pPoet = BuildPoet(poet_dict).build_poet()
		poet_obj_list.append(pPoet)
	return poet_obj_list
