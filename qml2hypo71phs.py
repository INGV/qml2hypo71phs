##################################################################
##################################################################
##################################################################
##################################################################
### This python3 code contains the parsing part only for full qml
### to extrant any info e put it into a json object.
### The json object is only a facility.
### The key features are
### - Arguments allow to input file or eventid for webservice
### - Arguments have defaults
### - The extracted informations are packed into a jason object 
###   (originally designed by Ivano Carluccio) for any further use
###
### This part and the input arguments can be then completed by a
### output formatter to anything

### IMPORTING LIBRARIES
import os,argparse,subprocess,copy,pwd,socket,time
import sys
if sys.version_info[0] < 3:
   reload(sys)
   sys.setdefaultencoding('utf8')
import math
import decimal
import json
from xml.etree import ElementTree as ET
from six.moves import urllib
from datetime import datetime

## the imports of Obspy are all for version 1.1 and greater
from obspy import read, UTCDateTime
from obspy.core.event import Catalog, Event, Magnitude, Origin, Arrival, Pick
from obspy.core.event import ResourceIdentifier, CreationInfo, WaveformStreamID
try:
    from obspy.core.event import read_events
except:
    from obspy.core.event import readEvents as read_events

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def parseArguments():
        parser=MyParser()
        parser.add_argument('--qmlin', help='Full path to qml event file')
        parser.add_argument('--eventid', help='INGV event id')
        parser.add_argument('--version', default='preferred',help="Agency coding origin version type (default: %(default)s)\n preferred,all, or an integer for known version numbers")
        parser.add_argument('--conf', default='./ws_agency_route.conf', help="needed with --eventid\n agency webservices routes list type (default: %(default)s)")
        parser.add_argument('--agency', default='ingv', help="needed with --eventid\n agency to query for (see routes list in .conf file) type (default: %(default)s)")
        if len(sys.argv) <= 1:
            parser.print_help()
            sys.exit(1)
        args=parser.parse_args()
        return args
# Nota: per aggiungere scelte fisse non modificabili usa choices=["known_version_number","preferred","all"]

try:
    import ConfigParser as cp
    #sys.stderr.write("ConfigParser loaded\n")
except ImportError:
    #sys.stderr.write("configparser loaded\n")
    import configparser as cp

# Build a dictionary from config file section
def get_config_dictionary(cfg, section):
    dict1 = {}
    options = cfg.options(section)
    for option in options:
        try:
            dict1[option] = cfg.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


# JSON ENCODER CLASS
class DataEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)

        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

def json_data_structure():
    null="null"
    event = {"data": {"event": {
            "id_locator": 0,
            "type_event": null,
            "provenance_name": null,
            "provenance_instance": null,
            "provenance_softwarename": self_software,
            "provenance_username": null,
            "provenance_hostname": null,
            "provenance_description": url_to_description,
            "hypocenters": []}}}
    hypocenter = {
            "ot": null,
            "lat": null,
            "lon": null,
            "depth": null,
            "err_ot": null,
            "err_lat": null,
            "err_lon": null,
            "err_depth": null,
            "err_h": null,
            "err_z": null,
            "confidence_lev": null,
            "e0_az": null,
            "e0_dip": null, 
            "e0": null,
            "e1_az": null,
            "e1_dip": null,
            "e1": null,
            "e2_az": null,
            "e2_dip": null,
            "e2": null,
            "fix_depth": null,
            "min_distance": null,
            "max_distance": null,
            "azim_gap": null,
            "sec_azim_gap": null,
            "rms": null,
            "w_rms": null,
            "is_centroid": null,
            "nph": null,
            "nph_s": null,
            "nph_tot": null,
            "nph_fm": null,
            "quality": null,
            "type_hypocenter": "",
            "model": null,
            "loc_program": null,
            "provenance_name": null,
            "provenance_instance": null,
            "provenance_softwarename": self_software,
            "provenance_username": null,
            "provenance_hostname": null,
            "provenance_description": url_to_description,
            "magnitudes": [],
            "phases": []
        }
    magnitude = {
              "mag": null,
              "type_magnitude": null,
              "err": null,
              "mag_quality": null, #?
              "quality": null, #?
              "nsta_used": null,
              # From StationsMag or Amplitude
              "nsta": null,
              "ncha": null,
              # From Boh
              "min_dist": null,
              "azimut": null,
              "provenance_name": null,
              "provenance_instance": null,
              "provenance_softwarename": self_software,
              "provenance_username": null,
              "provenance_hostname": null,
              "provenance_description": url_to_description,
              "amplitudes": []
            }

    amplitude = {
                  "time1": null,
                  "amp1": null,
                  "period1": null,
                  "time2": null,
                  "amp2": null,
                  "period2": null,
                  "type_amplitude": null,
                  "mag": null,
                  "type_magnitude": null,
                  "scnl_net": null,
                  "scnl_sta": null,
                  "scnl_cha": null,
                  "scnl_loc": null, 
                  #"ep_distance": 694,
                  #"hyp_distance": 0, ??
                  # "azimut": 161, ??
                  # "err_mag": 0,
                  # "mag_correction": 0,
                  "is_used": null,
                  "provenance_name": null,
                  "provenance_instance": null,
                  "provenance_softwarename": self_software,
                  "provenance_username": null,
                  "provenance_hostname": null,
                  "provenance_description": url_to_description
                }

    phase = {
              "isc_code": null,
              "weight_picker": null,
              "arrival_time": null,
              "err_arrival_time": null,
              "firstmotion": null,
              "emersio": null,
              "pamp": null,
              "scnl_net": null,
              "scnl_sta": null,
              "scnl_cha": null,
              "scnl_loc": null,
              "ep_distance": null,
              "hyp_distance": null,
              "azimut": 140,
              "take_off": 119,
              "polarity_is_used": null,
              "arr_time_is_used": null,
              "residual": -0.12,
              "teo_travel_time": null,
              "weight_phase_a_priori": null,
              "weight_phase_localization": null,
              "std_error": null,
              "provenance_name": "INGV",
              "provenance_instance": "BULLETIN-INGV",
              "provenance_softwarename": self_software,
              "provenance_username": null,
              "provenance_hostname": null,
              "provenance_description": url_to_description
            }
    return event,hypocenter,magnitude,amplitude,phase
    
# Get QuakeML Full File from webservice
def getqml(event_id,bu,op):
    urltext=bu + "query?eventid=" + str(event_id) + op
    #urltext=bu + "query?eventid=" + str(event_id) + "&includeallmagnitudes=true&includeallorigins=true&includearrivals=true&includeallstationsmagnitudes=true"
    try:
        req = urllib.request.Request(url=urltext)
        try:
            res = urllib.request.urlopen(req)
        except Exception as e:
            print("Query in urlopen")
            if sys.version_info[0] >= 3:
               print(e.read()) 
            else:
               print(str(e))
            sys.exit(1)
    except Exception as e:
        print("Query in Request")
        if sys.version_info[0] >= 3:
           print(e.read()) 
        else:
           print(str(e))
        sys.exit(1)
    return res.read(),urltext

#################### END OF QML PARSER COMMON PART ###########################
###### FROM HERE ON ADD ON PURPOSE OUTPUT FORMATTERS #########################

############# HYPO71 PHASE FILE ##############################################
# Back Conversions are taken from https://gitlab.rm.ingv.it/adsdbs/seisev/blob/master/startingpoint/1_0_1/skeleton.sql#L15628 
def convert_sispick_quality(q):
    qf=float(q)
    if qf <= 0.1:
        w='0'
    elif qf > 0.1 and qf <= 0.3:
        w='1'
    elif qf > 0.3 and qf <= 0.6:
        w='2'
    elif qf > 0.6 and qf <= 1.0:
        w='3'
    elif qf > 1.0 and qf <= 3.0:
        w='4'
    elif qf > 3.0:
        w='8'
    return w

def polarity_qml2hypo(qpp):
    if qpp == "positive":
       p='U'
    elif qpp == "negative":
       p='D'
    elif qpp == "undecidable":
       p=''
    return p


def onset_qml2hypo(qpo):
    if qpo == "impulsive":
       o = 'i'
    elif qpo == "emergent":
       o = 'e'
    elif qpo == "questionable":
       o = ''
    return o

def set_format(a,p):
    if a < 10:
         af="%3.1f" 
    elif a >= 10 and a < 100:
         af="%3.0f"
    elif a >= 100 and a < 1000:
         af="%3i"
    if p < 10:
         pf="%3.1f" 
    elif p >= 10 and p < 100:
         pf="%3.0f"
    elif p >= 100 and p < 1000:
         pf="%3i"
    return af,pf

def to_hypoinverse(pP,pS,a,eid,oid,ver):
    # https://escweb.wr.usgs.gov/content/software/HYPOINVERSE/doc/hyp1.40.pdf
    # ftp://ehzftp.wr.usgs.gov/klein/hyp1.41/hyp1.41-release-notes.pdf (updated 2015)
    # The output format described in the above pdf is the classical hypo71 phase file implemented in hypoinverse with additional information
    phs=[]
    for k,v in pP.items():
        hi_line = "x" * 110
        p_used=True if v[7] == '1' else False
        p_tim = UTCDateTime(v[6])
        if p_used:
           pol=" " if v[4] == "null" or v[4] == "" else v[4]
           wei=" " if v[5] == "null" or v[5] == "" else v[5]
           if v[8] == "null" or v[8] == "":
              com=" "
              cha="---"
           else:
              com=v[8][2] if len(v[8]) == 3 else " "
              cha=v[8]
           Ptime="%2.2i%2.2i%2.2i%2.2i%2.2i%05.2f" % (int(str(p_tim.year)[2:4]),p_tim.month,p_tim.day,p_tim.hour,p_tim.minute,(float(p_tim.second) + float(p_tim.microsecond)/1000000.))
           if len(v[0]) == 4:
              hi_line = v[0] + "x" + v[3] + pol + wei + com + Ptime + hi_line[24:]
           elif len(v[0]) == 5:
              hi_line = v[0][0:4] + "x" + v[3] +  pol + wei + com + Ptime + hi_line[24:77] + v[0][4] + hi_line[78:]
           elif len(v[0]) == 3:
              hi_line = v[0] + "xx" + v[3] + pol + wei + com + Ptime + hi_line[24:]
           try:
               s_used=True if pS[k][7] == '1' else False
           except:
               s_used=False
               pass
           if s_used:
              s_tim = UTCDateTime(pS[k][6])
              s_seconds = float((int(s_tim.minute)-int(p_tim.minute))*60.) + float((float(s_tim.second)+float(s_tim.microsecond)/1000000.))
              fmt = "%05.2f" if s_seconds < 100 else "%05.1f" # if the S seconds are >= 100 the format is modified to keep alignment
              weis = " " if pS[k][5] == "null" or pS[k][5] == "" else pS[k][5]
              hi_line = hi_line[:31] + fmt % (s_seconds) + "x" + pS[k][3] + "x" + weis + hi_line[40:]
           hi_line = hi_line[:78] + cha + v[1] + v[2] + hi_line[85:]
           try:
              ka_n=k + "_" + v[8][0:2] + "N"
              ka_e=k + "_" + v[8][0:2] + "E"
              # The QML INGV AML channel Amplitude is half of peak to peak while hypo71/hypoinverse/hypoellipse is peak-to-peak so ...
              # here for clarity channel amp (here already in mm) is multiplied by 2 then the two channel peak-to-peak amps are summed 
              # and the mean is caculated to be written in f3.0 from column 43
              hi_amp= ((float(a[ka_n][4])*2 + float(a[ka_e][4])*2)/2) 
              # first I used one of the two periods, float(a[ka_n][4]), now the mean ... is it correct?
              hi_per= (float(a[ka_n][5]) + float(a[ka_e][5]))/2 
              amp_present=True
              fa,fp = set_format(hi_amp,hi_per)
              hi_line = hi_line[:44] + fa % (hi_amp) + fp % (hi_per) + hi_line[50:]
           except Exception as e:
              amp_present=False
              pass
           idlen=len(str(eid))
           oridlen=len(str(or_id))
           verlen=len(str(ver))
           hi_line=hi_line.replace('x',' ')
           hi_line=hi_line[:89] + "EVID:" + str(eid) + ",ORID:" + str(oid) + ",V:" + str(ver)
           # For information completeness, 
           # both the peak-to-peak channel amplitudes are reported in free format at the end of the line
           try: 
               all_amps=[ v for k,v in a.items() if k.startswith(ka_n[:-3])]
           except:
               all_amps=[]
           if len(all_amps) > 0:
              for la in all_amps:
                  hi_line=hi_line + "," + str(la[3]) + ":" + str(float(la[4])*2)
              #hi_line=hi_line + ",AN:" + str(float(a[ka_n][4])*2) + ",AE:" + str(float(a[ka_e][4])*2)
           
           phs.append(hi_line)
           #hi_file_out.write(hi_line)
    if len(phs) != 0:
       phs.append('') # Terminator line for free 1st trial location
    return phs 
    #hi_file_out.close() 
#Start Fortran
#Col. Len. Format Data
#1 4 A4 4-letter station site code. Also see col 78.
#5 2 A2 P remark such as "IP". If blank, any P time is ignored.
#7 1 A1 P first motion such as U, D, +, -, C, D.
#8 1 I1 Assigned P weight code.
#9 1 A1 Optional 1-letter station component.
#10 10 5I2 Year, month, day, hour and minute.
#20 5 F5.2 Second of P arrival.
#25 1 1X Presently unused.
#26 6 6X Reserved remark field. This field is not copied to output files.
#32 5 F5.2 Second of S arrival. The S time will be used if this field is nonblank.
#37 2 A2, 1X S remark such as "ES".
#40 1 I1 Assigned weight code for S.
#41 1 A1, 3X Data source code. This is copied to the archive output.
#45 3 F3.0 Peak-to-peak amplitude in mm on Develocorder viewer screen or paper record.
#48 3 F3.2 Optional period in seconds of amplitude read on the seismogram. If blank, use the standard period from station file.
#51 1 I1 Amplitude magnitude weight code. Same codes as P & S.
#52 3 3X Amplitude magnitude remark (presently unused).
#55 4 I4 Optional event sequence or ID number. This number may bereplaced by an ID number on the terminator line.
#59 4 F4.1 Optional calibration factor to use for amplitude magnitudes. If blank, the standard cal factor from the station file is used.
#63 3 A3 Optional event remark. Certain event remarks are translated into 1-letter codes to save in output.
#66 5 F5.2 Clock correction to be added to both P and S times.
#71 1 A1 Station seismogram remark. Unused except as a label on output.
#72 4 F4.0 Coda duration in seconds.
#76 1 I1 Duration magnitude weight code. Same codes as P & S.
#77 1 1X Reserved.
#78 1 A1 Optional 5th letter of station site code.
#79 3 A3 Station component code.
#82 2 A2 Station network code.
#84-85 2 A2 2-letter station location code (component extension)

    #print('#### Not Used Picks ############')
    #for k,v in pick_P.items():
    #    p_not_used=True if v[-1] == '0' else False
    #    if p_not_used:
    #       print(v)
    #       try:
    #           s_not_used=True if pick_S[k][-1] == '0' else False
    #       except:
    #           s_not_used=False
    #           pass
    #       if s_used:
    #          print(pick_S[k])
           #if s_used == '1':
#    print(linea['PLONS_P_1'])
#    if len(linea['PLONS_P_1'][0]) > 4:
#       fase = str(linea['PLONS_P_1'][0][0:4])
#    print(type(fase),fase)

################## MAIN ####################
args=parseArguments()

# Getting this code name
self_software=sys.argv[0]

# If a qml input file is given, file_qml is the full or relative path_to_file
if args.qmlin:
   qml_ans=args.qmlin
   url_to_description = "File converted from qml file " + args.qmlin.split(os.sep)[-1]

# This is the version that will be retrieved from the qml
orig_ver=args.version

# If qmlin is not given and an eventid is given, file_qml is the answer from a query and the configuration file is needed
if args.eventid:
   eid=args.eventid
   # Now loading the configuration file
   if os.path.exists(args.conf) and os.path.getsize(args.conf) > 0:
      paramfile=args.conf
   else:
      print("Config file " + args.conf + " not existing or empty")
      sys.exit(2)
   confObj = cp.ConfigParser()
   confObj.read(paramfile)
   # Metadata configuration
   agency_name = args.agency.lower()
   try:
       ws_route = get_config_dictionary(confObj, agency_name)
   except Exception as e:
       if sys.version_info[0] >= 3:
          print(e) 
       else:
          print(str(e))
       sys.exit(1)
   # Now requesting the qml file from the webservice
   qml_ans, url_to_description = getqml(eid,ws_route['base_url'],ws_route['in_options'])
   if not qml_ans or len(qml_ans) == 0:
      print("Void answer with no error handling by the webservice")
      sys.exit(1)

if not args.qmlin and not args.eventid:
       print("Either --qmlin or --eventid are needed")
       sys.exit()

# Now reading in qml to obspy catalog
try:
    cat = read_events(qml_ans)
except Exception as e:
    if sys.version_info[0] >= 3:
       print(e) 
    else:
       print(str(e))
       print("Error reading cat")
    sys.exit(1)
###################################
# Lista delle chiavi del full qml #
###################################
# focal_mechanisms ----------< Ok
# origins ----------< Ok
# picks ----------< Ok
# magnitudes ----------< Ok
# station_magnitudes ----------< Ok
# amplitudes ----------< Ok

# resource_id ----------< Ok
# creation_info ----------< Ok
# event_descriptions ----------< Ok
# event_type ----------< Ok
# event_type_certainty ----------< Ok
# comments ----------< Ok
# _format ----------< Ok

# ----------------------------- #
# i seguenti non li parso       #
# preferred_magnitude_id        #
# preferred_focal_mechanism_id  #
# preferred_origin_id           #
# ----------------------------- #

event,hypocenter,magnitude,amplitude,phase = json_data_structure()
#print(event,hypocenter,magnitude,amplitude,phase)
EARTH_RADIUS=6371 # Defined after eventdb setup (valentino.lauciani@ingv.it)
DEGREE_TO_KM=111.1949 # Defined after eventdb setup (valentino.lauciani@ingv.it)



########## FROM HERE THE PART OF MAIN HANDLING SPECIFICALLY TO OUTPUT HYPO71PHS
for ev in cat:
    evdict=dict(ev)
    #for k, v in evdict.items():
        #print(k, v)
    #pref_mag=evdict['magnitudes'][0]['mag']
    #region=evdict['event_descriptions'][0].text
    eid=str(evdict['resource_id']).split('=')[-1]
    
    # Ottengo gli ID delle versioni preferite
    pref_or_id=str(evdict['preferred_origin_id']).split('=')[-1]
    pref_ma_id=str(evdict['preferred_magnitude_id']).split('=')[-1]
    pref_fm_id=str(evdict['preferred_focal_mechanism_id']).split('=')[-1]
    # Se non la versione cercata e' la preferita, il numero diversione diventa l'id della preferita
    orig_ver_id=False
    if orig_ver.lower() == 'preferred':
       orig_ver_id = pref_or_id
       #print("Preferred was asked: ",orig_ver_id)
    #print('----------- Event Info Start --------')
    #print(evdict['resource_id'])
    #print(evdict['creation_info'])
    #print(evdict['event_descriptions'])
    #print(evdict['event_type'])
    #print(evdict['event_type_certainty'])
    #print(evdict['comments'])
    #print(evdict['_format'])
    #print('----------- Event Info End ----------')
    eo = copy.deepcopy(event) 
    eo["id_locator"] = str(evdict['resource_id']).split('=')[-1]
    eo["type_event"] = evdict['event_type']
#CreationInfo(agency_id='INGV', author='hew1_mole#MOD_EQASSEMBLE', creation_time=UTCDateTime(2012, 5, 29, 7, 19, 57))
    eo["provenance_name"] = evdict['creation_info']['agency_id']
    eo["provenance_instance"] = evdict['creation_info']['author']
    #print(eo)
    version_found=False
    for origin in evdict['origins']:
        or_id=str(origin['resource_id']).split('=')[-1]
        # Se esiste una versione dentro le creation info allora si legge il valore altrimetni e' falso.
        try:
            or_info_version = origin['creation_info']['version']
        except:
            or_info_version = False
        # Se la versione chiesta e' la preferita vince il primo check che e' fatto sull'origin id e non sul numero di versione
        if str(orig_ver_id) == or_id or or_info_version == str(orig_ver) or str(orig_ver) == 'all' or str(orig_ver) == 'All' or str(orig_ver) == 'ALL':
           or_id_to_write=or_id
           version_name=or_info_version
           version_found=True
           #print(version_found,orig_ver_id)
           #for k, v in origin.items():
           #    print(k,v)
           #print(origin)
           oo = copy.deepcopy(hypocenter)
           try:
               oo['ot'] = str(origin['time'])
           except:
               pass
           try:
               oo['lat'] = origin['latitude']
           except:
               pass
           try:
               oo['lon'] = origin['longitude']
           except:
               pass
           try:
               oo['depth'] = origin['depth']
           except:
               pass
           if origin['depth_type'] == 'from location':
              oo['fix_depth'] = 0
           else:
              oo['fix_depth'] = 1
           # space time coordinates errors
           try:
               oo['err_ot']=origin['time_errors']['uncertainty']
           except:
               pass
           try:
               oo['err_lat']=(float(origin['latitude_errors']['uncertainty'])*(EARTH_RADIUS*2*math.pi))/360. # from degrees to km
           except:
               pass
           try:
               oo['err_lon']=(float(origin['longitude_errors']['uncertainty'])*EARTH_RADIUS*math.cos(float(origin['latitude'])*2*(math.pi/360.))*2*math.pi)/360. # from degrees to km
           except:
               pass
           try:
               oo['err_depth']=float(origin['depth_errors']['uncertainty'])/1000.
           except:
               pass
           try:
               oo['err_h'] = float(origin['origin_uncertainty']['horizontal_uncertainty'])/1000.
           except:
               pass
           try:
               oo['err_z'] = oo['err_depth']
           except:
               pass
           ######### i prossimi tre valori commentati sono legati in modo NON bidirezionale ai valori dell'ellissoide
           #1 min_ho_un = origin['origin_uncertainty']['min_horizontal_uncertainty']
           #2 max_ho_un = origin['origin_uncertainty']['max_horizontal_uncertainty']
           #3 az_max_ho_un = origin['origin_uncertainty']['azimuth_max_horizontal_uncertainty']
           #4 pref_desc = origin['origin_uncertainty']['preferred_description']
           try:
               oo['confidence_lev'] = origin['origin_uncertainty']['confidence_level']
           except:
               pass
           try:
               oo['min_distance'] = origin['quality']['minimum_distance']
           except:
               pass
           try:
               oo['max_distance'] = origin['quality']['maximum_distance']
           except:
               pass
           try:
               oo['azim_gap'] = origin['quality']['azimuthal_gap']
           except:
               pass
           try:
               oo['rms'] = origin['quality']['standard_error']
           except:
               pass
           try:
               oo['model'] = origin['earth_model_id']
           except:
               pass
           oo['provenance_name'] = origin['creation_info']['agency_id']
           oo['provenance_istance'] = origin['creation_info']['author']
           #oo[''] = origin['quality']['']
           #sys.exit()
    #    print(origin['creation_info']['version'])
           P_count_all=0
           S_count_all=0
           P_count_use=0
           S_count_use=0
           Pol_count=0
           pick_P = {}
           pick_S = {}
           arrivals=list(origin['arrivals'])
           for pick in evdict['picks']:
               po = copy.deepcopy(phase)
               #for k, v in pick.items():
               #    print(k,v)
               po['arr_time_is_used']=0
               pick_id=str(pick['resource_id']).split('=')[-1]
               try:
                   po['isc_code']      = pick['phase_hint']
               except:
                   pass
               try:
                   po['scnl_net']      = pick['waveform_id']['network_code']
               except:
                   pass
               try:
                   po['scnl_sta']      = pick['waveform_id']['station_code']
               except:
                   pass
               try:
                   po['scnl_cha']      = pick['waveform_id']['channel_code']
               except:
                   pass
               try:
                   po['arrival_time']  = pick['time']
               except:
                   pass
               try:
                   po['weight_picker'] = convert_sispick_quality(pick['time_errors']['uncertainty'])
               except:
                   low_unc=float(pick['time_errors']['lower_uncertainty'])
                   up_unc=float(pick['time_errors']['upper_uncertainty'])
                   po['weight_picker'] = convert_sispick_quality((low_unc+up_unc))
               try:
                   po['firstmotion']   = polarity_qml2hypo(pick['polarity'])
               except:
                   pass
               try:
                   po['emersio']       = onset_qml2hypo(pick['onset'])
               except:
                   pass
               try:
                   if pick['waveform_id']['location_code'] == "":
                      po['scnl_loc'] = "--"
                   else:
                      po['scnl_loc'] = pick['waveform_id']['location_code']
               except:
                   pass
               try:
                   if pick['polarity'] != "undecidable" and pick['polarity'] != "":
                      Pol_count += 1
               except:
                   pass
               #print(arrival)
               #print(pick)
               for arrival in arrivals:
                   #for k, v in arrival.items():
                   #    #print(k)
                   #    print(k, v)
                   a_pick_id=str(arrival['pick_id']).split('=')[-1]
                   if a_pick_id == pick_id:
                      try:
                          po['arr_time_is_used']=1
                      except:
                          pass
                      #print(pick_id,a_pick_id,pick['waveform_id']['station_code'],pick['phase_hint'],po['arr_time_is_used'])
                      try:
                          po['isc_code']      = arrival['phase'][0]
                      except:
                          pass
                      #print("SI ",arrival['phase'],pick['time'],pick['waveform_id']['station_code'])
                      try:
                          po['ep_distance']   = float(arrival['distance'])*111.1949 # questo calcolo e' approssimato e non rapportato alla latitudone
                      except:
                          po['ep_distance']   = arrival['distance']
                      try:
                          po['azimut']        = arrival['azimuth']
                      except:
                          pass
                      try:
                          po['take_off']      = arrival['takeoff_angle']
                      except:
                          pass
                      try:
                          po['weight_phase_localization'] = arrival['time_weight']
                      except:
                          pass
                      try:
                          po['residual'] = arrival['time_residual']
                      except:
                          pass
                      try:
                          if arrival['phase'][0] == 'P' or arrival['phase'][0] == 'p':
                             P_count_all += 1 
                             if arrival['time_weight'] > 0:
                                P_count_use += 1
                      except:
                          pass
                      try:
                          if arrival['phase'][0] == 'S' or arrival['phase'][0] == 's':
                             S_count_all += 1 
                             if arrival['time_weight'] > 0:
                                S_count_use += 1
                      except:
                          pass
               #print(pick_id,a_pick_id,pick['waveform_id']['station_code'],pick['phase_hint'],po['arr_time_is_used'])
               # Writing the Pick into the picks dictionary based on the sta and net key (for reuse in formatting steps)
               if po['arr_time_is_used'] == 1:
                  pick_key= str(po['scnl_net']) + "_" + str(po['scnl_sta'])
                  if str(po['isc_code']).lower() == 'p':
                     pick_P[str(pick_key)] = [str(po['scnl_sta']),str(po['scnl_net']),str(po['scnl_loc']),str(po['isc_code']),str(po['firstmotion']),str(po['weight_picker']),str(po['arrival_time']),str(po['arr_time_is_used']),str(po['scnl_cha'])]
                  if str(po['isc_code']).lower() == 's':
                     pick_S[str(pick_key)] = [str(po['scnl_sta']),str(po['scnl_net']),str(po['scnl_loc']),str(po['isc_code']),str(po['firstmotion']),str(po['weight_picker']),str(po['arrival_time']),str(po['arr_time_is_used']),str(po['scnl_cha'])]
                  oo["phases"].append(po)
           oo['nph'] = P_count_use+S_count_use
           oo['nph_s'] = S_count_use
           oo['nph_tot'] = P_count_all+S_count_all
           oo['nph_fm'] = Pol_count
           amps = {}
           for mag in evdict['magnitudes']:
               m_or_id=str(mag['origin_id']).split('=')[-1]
               if m_or_id == or_id:
                  mm = copy.deepcopy(magnitude)
                  #for k, v in mag.items():
                  #    print(k, v)
                  #pass
                  mm['mag'] = mag['mag']
                  mm['type_magnitude'] = mag['magnitude_type']
                  mm['err'] = mag['mag_errors']['uncertainty']
                  mm['nsta_used'] = mag['station_count']
                  mm['provenance_name'] = mag['creation_info']['agency_id']
                  mm['provenance_instance'] = mag['creation_info']['author']
                  #print(mm['mag'],mm['type_magnitude'])
                  for sta_mag in evdict['station_magnitudes']:
                      sm_or_id=str(sta_mag['origin_id']).split('=')[-1]
                      sm_am_id=str(sta_mag['amplitude_id']).split('=')[-1]
                      if sm_or_id == or_id:
                         #print(sta_mag)
                         am = copy.deepcopy(amplitude)
                         am['type_magnitude'] = sta_mag['station_magnitude_type']
                         am['mag'] = sta_mag['mag']
                         am['is_used'] = 1
                         #print(sta_mag)
                         #print(sta_mag['comments'])
                         #for k, v in sta_mag.items():
                         #    print(k, v)
                         for amp in evdict['amplitudes']:
                             #for k, v in amplitude.items():
                             #    print(k, v)
                             am_id=str(amp['resource_id']).split('=')[-1]
                             am_or_id=str(sta_mag['amplitude_id']).split('=')[-1]
                             if amp['unit'] == 'm':
                                a_mul=1000.
                             else:
                                a_mul=1.
                             if sm_am_id == am_id:
                                try:
                                    beg=float(amp['time_window']['begin'])
                                    end=float(amp['time_window']['end'])
                                    a_t_ref=amp['time_window']['reference']
                                    if beg == 0 and end != 0:
                                       am['time1'] = a_t_ref
                                       am['amp1'] = str(float(amp['generic_amplitude']))
                                       am['period1'] = amp['period']
                                    elif beg != 0 and end == 0:
                                       am['time2'] = a_t_ref
                                       am['amp2'] = str(float(amp['generic_amplitude']))
                                       am['period2'] = amp['period']
                                except:
                                    pass
                                am['type_amplitude'] = amp['type']
                                am['scnl_net'] = amp['waveform_id']['network_code']
                                am['scnl_sta'] = amp['waveform_id']['station_code']
                                am['scnl_cha'] = amp['waveform_id']['channel_code']
                                am['scnl_loc'] = amp['waveform_id']['location_code']
                                #print(am['scnl_net'],am['scnl_sta'],am['scnl_cha'])
                                try:
                                    am['provenance_instance'] = amp['creation_info']['author']
                                except:
                                    pass
                                try:
                                    am['provenance_name'] = amp['creation_info']['agency_id']
                                except:
                                    pass

                                amps_key= str(am['scnl_net']) + "_" + str(am['scnl_sta']) + "_" + str(am['scnl_cha'])
                                amps[str(amps_key)] = [str(am['scnl_sta']),str(am['scnl_net']),str(am['scnl_loc']),str(am['scnl_cha']),str(float(amp['generic_amplitude'])*float(a_mul)),str(amp['period'])]
                         mm["amplitudes"].append(am)
                  oo["magnitudes"].append(mm)
           eo["data"]["event"]["hypocenters"].append(oo) # push oggetto oo in hypocenters
    if not version_found:
       sys.stderr.write("Chosen version doesnt match any origin id")
       sys.exit(202) # Il codice 202 e' stato scelto per identificare il caso in cui tutto sia corretto ma non ci sia alcuna versione come quella scelta
    out_print=to_hypoinverse(pick_P,pick_S,amps,eid,or_id_to_write,version_name)
    for item in out_print:
        print(item)
sys.exit(0)
