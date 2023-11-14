from database import Database

DATABASE_PATH = "annotation.db"
db = Database(DATABASE_PATH)

# db.update_current_issue('ramtin_123', 352750519)
print(db.get_all_comment_annotations())
print(db.get_all_issue_annotations())
#
# db.create_user('bobby_123', 0, 352750519, 869840472, 352750519)
# db.create_user('ramtin_123', 0, '352750519', '352750519', '1165880637')
# db.create_user('imran_123', 0, '352750519', '352750519', '1165880637')

db.create_user('admin_db', 1, '', '', '')

db.create_user('alhabbalbh', 0, 352750519, 613337048, 352750519)
db.create_user('arevaloh', 0, 869840472, 549848681, 869840472)
db.create_user('barlowrm3', 0, 1100051808, 619762251, 1100051808)
db.create_user('bensont3', 0, 485217326, 1843328693, 485217326)
db.create_user('cortezaa2', 0, 1665591134, 1104666990, 1665591134)
db.create_user('daniyaers', 0, 774727384, 1227174892, 774727384)
db.create_user('estradab', 0, 1011467346, 628465400, 1011467346)
db.create_user('johnan', 0, 369840190, 1465034831, 369840190)
db.create_user('johnjm2', 0, 1418948680, 927966336, 1418948680)
db.create_user('keelymr', 0, 1118392130, 1331118596, 1118392130)
db.create_user('khanwg', 0, 1036757791, 348797250, 1036757791)
db.create_user('lizamamobj', 0, 498868764, 1417883451, 498868764)
db.create_user('lopezboutije', 0, 1346088769, 1004915962, 1346088769)
db.create_user('mahmoodm4', 0, 288780107, 936567326, 288780107)
db.create_user('mooremj8', 0, 1308973136, 724775047, 1308973136)
db.create_user('oatmankr', 0, 1149608900, 556620312, 1149608900)
db.create_user('olmsteadca', 0, 707573131, 722281859, 707573131)
db.create_user('patrickbn', 0, 286848335, 814840135, 286848335)
db.create_user('phungk2', 0, 362259981, 1314537659, 362259981)
db.create_user('riveragj', 0, 1170768726, 1166060886, 1170768726)
db.create_user('sakinf', 0, 1165880637, 276835188, 1165880637)

# Repeated
db.create_user('salkeyae', 0, 352750519, 613337048, 352750519)
db.create_user('siddiquiaa3', 0, 869840472, 549848681, 869840472)
db.create_user('smither3', 0, 1100051808, 619762251, 1100051808)
db.create_user('trandk2', 0, 485217326, 1843328693, 485217326)
db.create_user('weigandta', 0, 1665591134, 1104666990, 1665591134)
db.create_user('zeyarh', 0, 774727384, 1227174892, 774727384)
