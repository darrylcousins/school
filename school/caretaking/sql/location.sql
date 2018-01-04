USE ellesmere;
DELETE FROM caretaking_location;

SET IDENTITY_INSERT caretaking_location ON;

DECLARE @geom geometry;
DECLARE @validGeom geometry;
DECLARE @placemark geometry;

SET @geom = geometry::STPolyFromText('POLYGON((172.292355352632 -43.7573880109679, 172.292379673128 -43.7573889315891, 172.292356198318 -43.7577301307569, 172.292687591861 -43.7577445288953, 172.292686585636 -43.7577583968151, 172.292754427204 -43.7577609647148, 172.292762884788 -43.7576620887368, 172.29274745737 -43.7576624318226, 172.292773148997 -43.7573083378628, 172.29236219532 -43.7572937090396, 172.292355352632 -43.7573880109679))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(1, 'ABlock', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292490742623 -43.7575645303885, 172.292630181894 -43.7575707754189, 172.292640453804 -43.7573980282548, 172.292503144039 -43.757392830715, 172.292490742623 -43.7575645303885))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(2, 'ABlockCloister', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292483813104 -43.7576508051733, 172.292623920111 -43.7576570754605, 172.292630216879 -43.7575702932904, 172.292491340163 -43.7575655199197, 172.292483813104 -43.7576508051733))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(3, 'ABlockCommon', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292623649005 -43.7576562350866, 172.29274880183 -43.7576605076238, 172.292768172636 -43.75740239789, 172.292640487355 -43.7573975647827, 172.292623649005 -43.7576562350866))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(4, 'ABlockEast', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292767497485 -43.7574028371643, 172.292773648069 -43.7573091987061, 172.292360436145 -43.7572935575742, 172.292353643299 -43.7573871716698, 172.292767497485 -43.7574028371643))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(5, 'ABlockNorth', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292360484048 -43.7576458038634, 172.292354332672 -43.7577299651169, 172.292686678819 -43.7577426666117, 172.292692263636 -43.7576590583253, 172.292360484048 -43.7576458038634))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(6, 'ABlockSouth', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.29248444745 -43.7576505012147, 172.292503110391 -43.7573932941574, 172.292379241233 -43.757389069927, 172.292360577904 -43.757646277089, 172.29248444745 -43.7576505012147))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(7, 'ABlockWest', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292968830543 -43.7575010758536, 172.292983285753 -43.7572929686862, 172.292851153343 -43.7572883644331, 172.292836653639 -43.7574960730116, 172.292968830543 -43.7575010758536))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(8, 'Administration', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292240929808 -43.7577948854568, 172.292252269272 -43.7576459469507, 172.292106600301 -43.7576408181446, 172.292095288411 -43.7577893727308, 172.292240929808 -43.7577948854568))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(9, 'Art', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292346982576 -43.7579972979683, 172.292332970268 -43.757997173737, 172.292326267018 -43.7581072409097, 172.29228543994 -43.7581038413043, 172.292283097297 -43.7581538142264, 172.292324125616 -43.758154440249, 172.29231331372 -43.7582680601893, 172.29232483408 -43.7582684962858, 172.292315430938 -43.7583627012437, 172.2926648156 -43.7583768533152, 172.292670444983 -43.7582815785099, 172.292707330109 -43.7582835517171, 172.292725566051 -43.7580134108598, 172.29268747285 -43.7580115197143, 172.292693308946 -43.7579310857901, 172.292322152152 -43.7579172103438, 172.292317074185 -43.7579800362595, 172.292348640491 -43.7579816062161, 172.292346982576 -43.7579972979683))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(10, 'BBlock', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292599085812 -43.7581780162704, 172.292611353525 -43.7580086310179, 172.292453408076 -43.7580016657827, 172.29244255137 -43.758172929766, 172.292599085812 -43.7581780162704))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(11, 'BBlockCloister', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292435896512 -43.7582718008493, 172.292591710476 -43.7582796680675, 172.292599050197 -43.7581785073159, 172.292443477067 -43.7581723277474, 172.292435896512 -43.7582718008493))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(12, 'BBlockCommon', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.29272699711 -43.7580124801727, 172.292611342354 -43.7580090875988, 172.292592354742 -43.7582801848746, 172.292707401364 -43.7582825695758, 172.29272699711 -43.7580124801727))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(13, 'BBlockEast', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.2923233163 -43.7582689215052, 172.292316461975 -43.7583633852509, 172.292662387575 -43.7583767453997, 172.292668911467 -43.7582817355673, 172.2923233163 -43.7582689215052))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(14, 'BBlockSouth', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292454140359 -43.7582734055508, 172.292475394576 -43.7580017179789, 172.292332667158 -43.7579966406187, 172.292325408826 -43.7581057060729, 172.29228423514 -43.7581041475524, 172.292281326609 -43.7581532642096, 172.292321881049 -43.7581543259248, 172.292313224612 -43.7582688563164, 172.292454140359 -43.7582734055508))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(15, 'BBlockWest', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291673942699 -43.7578942724123, 172.291679292605 -43.7578172346681, 172.291597203759 -43.757813647632, 172.291590910994 -43.757890546736, 172.291673942699 -43.7578942724123))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(16, 'Boiler', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292080351861 -43.7573296458147, 172.292174849473 -43.7573330030636, 172.292176860583 -43.7573033843648, 172.292082648091 -43.7573002359254, 172.292080351861 -43.7573296458147))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(17, 'Busbay', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292753737264 -43.7577608558216, 172.292760959879 -43.7576613107004, 172.292692769053 -43.7576587296386, 172.292685342581 -43.757758200934, 172.292753737264 -43.7577608558216))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(18, 'Canteen', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292016623279 -43.757472025024, 172.292022221406 -43.7573990989042, 172.291774063221 -43.7573894839654, 172.291768700832 -43.7574629732222, 172.292016623279 -43.757472025024))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(19, 'Careers', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291591583801 -43.7578910864765, 172.291588795295 -43.7579393202387, 172.291670152035 -43.7579431869587, 172.291673702503 -43.7578942633403, 172.291591583801 -43.7578910864765))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(20, 'CaretakerShed', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291846251238 -43.7576292439255, 172.291832238019 -43.7576277863932, 172.291809286444 -43.7579263602101, 172.292199629365 -43.7579420644241, 172.292205661998 -43.7578412425217, 172.292237528581 -43.7578443029792, 172.292253098442 -43.7576474271635, 172.292216044756 -43.7576450974346, 172.292220931529 -43.7575423780171, 172.291852485706 -43.7575256484679, 172.291846251238 -43.7576292439255))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(21, 'CBlock', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292103246938 -43.75770214785, 172.292109789363 -43.7576119908326, 172.291960969834 -43.7576058734774, 172.291953127143 -43.757695497849, 172.292103246938 -43.75770214785))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(22, 'CBlockCloister', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292096855196 -43.7577898170189, 172.292092841637 -43.7578377861024, 172.292237420016 -43.7578432585973, 172.292240398278 -43.7577948653423, 172.292096855196 -43.7577898170189))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(23, 'CBlockFoyer', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.294882654475 -43.7595451356631, 172.29462929507 -43.7595369099936, 172.294753877239 -43.7575158843604, 172.294185821797 -43.7574976684913, 172.294210116882 -43.7571627096032, 172.293992492717 -43.7571562407694, 172.293963888947 -43.7574937404414, 172.293274030604 -43.757466482956, 172.293302057167 -43.7571367650341, 172.291541731681 -43.7570776436812, 172.291319620037 -43.7599899144909, 172.294616900607 -43.7601086398959, 172.294631663323 -43.7599280194603, 172.294854763167 -43.7599359099049, 172.294882654475 -43.7595451356631))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(24, 'CollegeBoundary', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291573822366 -43.7581620408702, 172.291657146519 -43.7581655433749, 172.291660294142 -43.7581221713719, 172.291577185029 -43.7581190249302, 172.291573822366 -43.7581620408702))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(25, 'Containers', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291865226004 -43.7573926236355, 172.291862429688 -43.7574403791697, 172.291935925573 -43.75744219472, 172.291938651842 -43.7573954034169, 172.291865226004 -43.7573926236355))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(26, 'Counsellor', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291941856859 -43.7578324558969, 172.292092282184 -43.757838149884, 172.29210217122 -43.7577018604568, 172.291952277712 -43.7576961865855, 172.291941856859 -43.7578324558969))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(27, 'Design', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292692395731 -43.7584488096569, 172.292686290562 -43.7585244442184, 172.293026935557 -43.7585380509382, 172.293032934484 -43.7584603355344, 172.292692395731 -43.7584488096569))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(28, 'English', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292215444666 -43.7574827502193, 172.292256162694 -43.7574842916255, 172.292262984783 -43.7573902774655, 172.292222934337 -43.7573887613624, 172.292215444666 -43.7574827502193))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(29, 'ESOL', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292818355141 -43.7582551795273, 172.293067221805 -43.7582663325404, 172.293084731274 -43.7580110443003, 172.292836719907 -43.7580037721496, 172.292818355141 -43.7582551795273))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(30, 'Gym', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.293084436364 -43.758011053947, 172.293216449735 -43.7580160502933, 172.293224010254 -43.7579050284395, 172.293092982333 -43.7579000694278, 172.293084436364 -43.758011053947))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(31, 'GymChangingRoom', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292866822213 -43.757942406376, 172.292862317557 -43.7580044920023, 172.293084436392 -43.7580110540044, 172.293092982364 -43.7579000694763, 172.293023058129 -43.7578979175035, 172.293019343959 -43.7579482985681, 172.292866822213 -43.757942406376))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(32, 'GymFoyer', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.29308565806 -43.7578402417577, 172.293082367966 -43.7578867397145, 172.293187755475 -43.7578910851152, 172.293190644224 -43.7578444593698, 172.29308565806 -43.7578402417577))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(33, 'GymGarage', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.29308170459 -43.7580623234802, 172.293212266084 -43.7580669080986, 172.293216449701 -43.7580160502726, 172.293083943809 -43.7580110353153, 172.29308170459 -43.7580623234802))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(34, 'GymOffice', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292861217429 -43.7580051169604, 172.292836829676 -43.7580051209604, 172.292818718162 -43.7582547433313, 172.293068143451 -43.7582670629496, 172.293063734071 -43.7583099697669, 172.293292511054 -43.7583195647387, 172.293310599256 -43.7580702346449, 172.293213631515 -43.7580665648146, 172.293226577013 -43.7579059967395, 172.29302391041 -43.7578970177242, 172.293025935208 -43.7578397783807, 172.292876186908 -43.7578341762502, 172.292861217429 -43.7580051169604))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(35, 'Hall', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291716507767 -43.7581070473497, 172.291692953433 -43.7584190176129, 172.292198803743 -43.7584375071303, 172.292222307576 -43.7581261951247, 172.291716507767 -43.7581070473497))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(36, 'HBlock', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291866545393 -43.7581846037527, 172.292216716199 -43.7581979270197, 172.292221968102 -43.7581255492175, 172.291871603668 -43.7581122864094, 172.291866545393 -43.7581846037527))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(37, 'HBlockNorth', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291857561243 -43.7583099768977, 172.291852354514 -43.7583817252187, 172.292182226159 -43.7583942125265, 172.292187757038 -43.7583227245567, 172.291857561243 -43.7583099768977))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(38, 'HBlockSouth', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291711637109 -43.7581525897459, 172.291692109939 -43.7584197784641, 172.291794181507 -43.7584234251975, 172.291813947673 -43.7581559756842, 172.291711637109 -43.7581525897459))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(39, 'HBlockWest', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.293232326789 -43.7578281991372, 172.293241180025 -43.757706166813, 172.293112463696 -43.7577024899451, 172.29310271015 -43.7578226101988, 172.293232326789 -43.7578281991372))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(40, 'HealthCentre', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292011592842 -43.7576074438337, 172.292016480449 -43.7575326760299, 172.291851678553 -43.7575264368734, 172.291846105833 -43.757601404245, 172.292011592842 -43.7576074438337))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(41, 'HomeEconomics', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292011565063 -43.7576073481836, 172.292070560828 -43.757609676198, 172.292074707949 -43.7575347419707, 172.292016962263 -43.7575329659408, 172.292011565063 -43.7576073481836))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(42, 'Hospitality', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291543415242 -43.7583652982357, 172.291651025254 -43.7583693722384, 172.291654337561 -43.7583270502265, 172.29154648742 -43.7583229671083, 172.291543415242 -43.7583652982357))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(43, 'Hothouse', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292371705947 -43.7574792115166, 172.292496751723 -43.7574847607004, 172.292503366469 -43.7573935866782, 172.292377075627 -43.7573896229121, 172.292371705947 -43.7574792115166))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(44, 'LabA', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292497819721 -43.7574856174206, 172.292372773928 -43.7574800682162, 172.292369239946 -43.7575599307626, 172.292488650584 -43.7575652666513, 172.292497819721 -43.7574856174206))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(45, 'LabB', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292326109194 -43.7581076604157, 172.292446706976 -43.7581122249846, 172.292450058854 -43.7580192949153, 172.29233284242 -43.7580148583599, 172.292326109194 -43.7581076604157))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(46, 'LabC', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.29231600441 -43.7582313538035, 172.292440042698 -43.7582352322404, 172.292444349386 -43.7581602967637, 172.292323751536 -43.7581557322335, 172.29231600441 -43.7582313538035))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(47, 'LabP', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292688365694 -43.7579932330676, 172.292692941166 -43.7579301685217, 172.292322152152 -43.7579172103438, 172.292318137152 -43.7579797013892, 172.292688365694 -43.7579932330676))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(48, 'Library', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291587375217 -43.757939266492, 172.291670652171 -43.7579433946779, 172.29167912578 -43.7578170840481, 172.29159649371 -43.7578136207622, 172.291587375217 -43.757939266492))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(49, 'Maintenance', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291634175345 -43.7574260715358, 172.291628634313 -43.7575051843178, 172.29176600808 -43.757510691197, 172.291772072315 -43.757430679087, 172.291634175345 -43.7574260715358))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(50, 'Maori', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292215530904 -43.7585044646992, 172.292495878526 -43.7585153430054, 172.292501072146 -43.7584437635215, 172.292220337041 -43.7584331373064, 172.292215530904 -43.7585044646992))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(51, 'Math', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291942332674 -43.7578332438246, 172.291957433591 -43.7576324769671, 172.291832550334 -43.757627364665, 172.291817980575 -43.757828151654, 172.291942332674 -43.7578332438246))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(52, 'Metalshop', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292875307494 -43.7578332052753, 172.292867405618 -43.757942115233, 172.29301957076 -43.7579489358631, 172.293027165167 -43.7578378728064, 172.292875307494 -43.7578332052753))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(53, 'Music', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.293202122154 -43.7582067294103, 172.293301106637 -43.7582108323658, 172.293310783587 -43.7580706366033, 172.293212240255 -43.758067263889, 172.293202122154 -43.7582067294103))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(54, 'MusicRehearsal', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291774445157 -43.7573891867969, 172.291771436134 -43.757430649403, 172.291634397724 -43.7574269159547, 172.291628217097 -43.7575053877159, 172.291766260527 -43.7575111892288, 172.291769091896 -43.7574629516592, 172.292016069642 -43.7574723018658, 172.292022757683 -43.7573985875595, 172.291774445157 -43.7573891867969))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(55, 'OBlock', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292099727134 -43.7573840654762, 172.292092324708 -43.7574785003129, 172.292256517144 -43.7574843368546, 172.292262998612 -43.7573898946347, 172.292099727134 -43.7573840654762))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(56, 'PBlock', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292630661585 -43.7575706414797, 172.29275232626 -43.757576062489, 172.292758172953 -43.75749547121, 172.292636449374 -43.7574908643053, 172.292630661585 -43.7575706414797))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(57, 'Room1', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292317706591 -43.7583636571892, 172.292450821129 -43.7583670628224, 172.292457613324 -43.7582734466116, 172.292324499112 -43.7582700409426, 172.292317706591 -43.7583636571892))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(58, 'Room10', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292104695454 -43.7581224030704, 172.292099632327 -43.7581921762613, 172.292217053416 -43.7581986012994, 172.292221348448 -43.7581268188621, 172.292104695454 -43.7581224030704))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(59, 'Room12', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291924343578 -43.7581142555617, 172.291919136972 -43.7581860034873, 172.292051282901 -43.7581910060473, 172.29205740075 -43.7581192926306, 172.291924343578 -43.7581142555617))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(60, 'Room13', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292187976241 -43.7583222492104, 172.292076743265 -43.7583186985685, 172.292071632334 -43.7583891299713, 172.292183585751 -43.7583953481384, 172.292187976241 -43.7583222492104))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(61, 'Room14', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292030264246 -43.7583169390515, 172.29191543372 -43.7583125920554, 172.291910274776 -43.7583836817098, 172.292024194121 -43.7583879942497, 172.292030264246 -43.7583169390515))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(62, 'Room15', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291691898766 -43.7584209578145, 172.291794018455 -43.7584241637626, 172.291802290016 -43.7583353706937, 172.291697532004 -43.7583307447016, 172.291691898766 -43.7584209578145))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(63, 'Room16', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292390669061 -43.7584395341122, 172.292385506942 -43.7585106780568, 172.292496596362 -43.7585157155848, 172.292501052139 -43.7584437121591, 172.292390669061 -43.7584395341122))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(64, 'Room17', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292329125346 -43.7585090991047, 172.292333904251 -43.7584379406326, 172.292220474951 -43.7584333694794, 172.292215675923 -43.7585048047829, 172.292329125346 -43.7585090991047))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(65, 'Room18', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292909166678 -43.7584556041921, 172.292903937449 -43.7585331568695, 172.293027471115 -43.7585386928479, 172.293032762489 -43.758460281793, 172.292909166678 -43.7584556041921))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(66, 'Room19', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292760427081 -43.7574955564994, 172.292768286748 -43.7574027970445, 172.292640868917 -43.7573987909341, 172.29263526325 -43.7574916356939, 172.292760427081 -43.7574955564994))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(67, 'Room2', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292687152906 -43.7585242806524, 172.292804923081 -43.7585291225909, 172.292810465522 -43.7584527293711, 172.292693632836 -43.7584488985238, 172.292687152906 -43.7585242806524))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(68, 'Room20', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291701225213 -43.7583302244734, 172.291801426446 -43.7583346779153, 172.291808595579 -43.7582484833014, 172.291704653526 -43.7582452083118, 172.291701225213 -43.7583302244734))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(69, 'Room21', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291631558522 -43.7575045660644, 172.291766295332 -43.7575107072146, 172.29177210343 -43.7574306746667, 172.291636278978 -43.7574265124563, 172.291631558522 -43.7575045660644))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(70, 'Room22', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292016139684 -43.7574713376423, 172.292023425239 -43.757398612775, 172.29193865182 -43.7573954034385, 172.291934001224 -43.7574687115062, 172.292016139684 -43.7574713376423))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(71, 'Room23', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292092509929 -43.7574519901655, 172.292216666377 -43.7574566902867, 172.292222301795 -43.7573882539614, 172.292099445485 -43.7573840865463, 172.292092509929 -43.7574519901655))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(72, 'Room24', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292512880277 -43.7576518938369, 172.292505610837 -43.757736512715, 172.292618318296 -43.7577407785031, 172.292623215291 -43.7576577023893, 172.292512880277 -43.7576518938369))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(73, 'Room4', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292355650665 -43.7577316532983, 172.292479747167 -43.7577347175175, 172.292484703441 -43.7576508274152, 172.292360725291 -43.7576461350117, 172.292355650665 -43.7577316532983))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(74, 'Room5', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.29260330741 -43.758103458816, 172.292720523961 -43.75810789508, 172.292724830268 -43.7580329595123, 172.292609986146 -43.7580269804472, 172.29260330741 -43.758103458816))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(75, 'Room6', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292599000937 -43.7581783943735, 172.292713904353 -43.7581835593993, 172.292719337772 -43.7581086665014, 172.292604493567 -43.758102687412, 172.292599000937 -43.7581783943735))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(76, 'Room7', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292453016234 -43.7583679622042, 172.292577054942 -43.7583718405056, 172.292583846922 -43.7582782243402, 172.292458681374 -43.7582743032975, 172.292453016234 -43.7583679622042))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(77, 'Room9', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292284466197 -43.758105267957, 172.292280981414 -43.7581532971079, 172.292445535548 -43.7581595253546, 172.292447834084 -43.7581122676638, 172.292284466197 -43.758105267957))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(78, 'ScienceTech', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291706476271 -43.7582452773333, 172.291807636436 -43.7582491070763, 172.291813460434 -43.7581562610804, 172.291712252631 -43.758153089532, 172.291706476271 -43.7582452773333))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(79, 'SCR', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.2924869576 -43.7576509127298, 172.292482941423 -43.7577062682972, 172.29250886412 -43.7577072494256, 172.292512821212 -43.7576527079349, 172.2924869576 -43.7576509127298))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(80, 'ServerRoom', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.293072104672 -43.7582014518814, 172.293202122154 -43.7582067294103, 172.293212240255 -43.758067263889, 172.293081506501 -43.7580620107127, 172.293072104672 -43.7582014518814))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(81, 'Stage', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291764354698 -43.7578001011849, 172.291767095701 -43.7577594558407, 172.291695494102 -43.7577566124936, 172.291692353643 -43.7577970585394, 172.291764354698 -43.7578001011849))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(82, 'TechGarage', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.292213824991 -43.7576147088738, 172.292220797484 -43.7575405746541, 172.292074903908 -43.7575350516947, 172.292070315362 -43.7576096164501, 172.292213824991 -43.7576147088738))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(83, 'Textile', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291905367092 -43.758067430286, 172.291908954191 -43.7580146807609, 172.291798955377 -43.7580103425472, 172.291795608408 -43.7580631011699, 172.291905367092 -43.758067430286))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(84, 'TractorShed', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291570709332 -43.7581086898327, 172.291722502907 -43.7581146105389, 172.291726002078 -43.7580630754695, 172.29157434521 -43.7580570645458, 172.291570709332 -43.7581086898327))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(85, 'VanGarage', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.293064364945 -43.7583096735966, 172.293292793369 -43.7583186149914, 172.29330061404 -43.7582108137777, 172.293071612031 -43.7582014333501, 172.293064364945 -43.7583096735966))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(86, 'WilsonRoom', @placemark);

SET @geom = geometry::STPolyFromText('POLYGON((172.291817837747 -43.7578277924327, 172.29181034524 -43.7579260296202, 172.292198341103 -43.7579411012991, 172.292205499991 -43.7578424354177, 172.291817837747 -43.7578277924327))', 3857).MakeValid();
SET @validGeom = @geom.MakeValid().STUnion(@geom.STStartPoint());
SET @placemark = @validGeom;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(87, 'Woodshop', @placemark);
SET IDENTITY_INSERT caretaking_location OFF;
