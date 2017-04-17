###############################################################################
# pySqlite2json :
# import sqlite file and query data
# convert to json
###############################################################################

# search bus number:
# SELECT bus_line, bus_start, bus_stop
# FROM busline
# WHERE bus_line = '"+ busline + "' AND bus_direction_en = 'inbound'

# search bus stop: 6808
# id, stop_name, stop_name_en, latitude, longitude
# SELECT id
# FROM busstop
# WHERE stop_name = '"+ busstop + "'"

# SELECT bus_line, bus_start, bus_stop
# FROM busline
# WHERE busstop_list like '%,"+ busstop_id + ",%'"

# import library
import sqlite3
import json

import codecs

def query_busstop(c):
  # initial variable
  list_busstop_id = []
  list_busstop_stopname = []
  list_busstop_stopname_en = []
  list_busstop_latitude = []
  list_busstop_longitude = []

  busstop_select = "bus_line, bus_start, bus_stop, bus_start_en, bus_stop_en, bus_direction, bus_direction_en"

  str_busstop_json = str()
  str_buslist_json = str()

  # find busline list for each busstop
  for row in c.execute("SELECT * FROM busstop"):
    # print(row[0], row[1], row[2], row[3], row[4])
    list_busstop_id.append(str(row[0]))
    list_busstop_stopname.append(row[1])
    list_busstop_stopname_en.append(row[2])
    list_busstop_latitude.append(row[3])
    list_busstop_longitude.append(row[4])

  for i in range(len(list_busstop_id)):
    # prepare for write json for busstop
    str_busstop_json += '"' + list_busstop_id[i] + '" :{ '
    str_busstop_json += '"stop_name" : "' + list_busstop_stopname[i] + '", '
    str_busstop_json += '"stop_name_en" : "' + list_busstop_stopname_en[i] + '", '
    str_busstop_json += '"latitude" : ' + list_busstop_latitude[i] + ', '
    str_busstop_json += '"longitude" : ' + list_busstop_longitude[i] + ', '
    str_busstop_json += '"bus" : ['

    # check query new busstop id
    for row2 in c.execute("SELECT " + busstop_select + " FROM busline WHERE busstop_list like '%," + list_busstop_id[i] + ",%'"):
      # print(row2[0], row2[1], row2[2], row2[3], row2[4])
      # check if have buslist in json
      if (len(str_buslist_json) > 0):
        str_buslist_json += ","
      # prepare for write json for buslist
      str_buslist_json += '{ "busline" : "' + row2[0] + '", '
      str_buslist_json += '  "busnname" : "' + row2[1] + " - " + row2[2] + '", '
      str_buslist_json += '  "busnname_en" : "' + row2[3] + " - " + row2[4] + '", '
      str_buslist_json += '  "direction" : "' + row2[5] + '", '
      str_buslist_json += '  "direction_en" : "' + row2[6] + '" }'

    # prepare for write json for buslist
    str_busstop_json += str_buslist_json
    str_buslist_json = str()

    str_busstop_json += ']'
    str_busstop_json += '}'
    
    # not last busline for each busstop
    if (i < len(list_busstop_id) - 1):
      str_busstop_json += ','

  # write json
  #with open('busstop.json', 'w') as outfile:  
  #  json.dump({'"busstop" : {" + str_busstop_json + "}'}, outfile)

  f = codecs.open('busstop.json', 'wb', "UTF-8")
  f.write(u'{"busstop" : {" + str_busstop_json + "}}')
  f.close()

  print("Finish Generate sqlite to json : busstop")

def query_busline(c):
  # initial variable
  list_busline_id = []
  list_busline_number = []
  list_busline_start = []
  list_busline_stop = []
  list_busline_direction = []
  list_busline_start_en = []
  list_busline_stop_en = []
  list_busline_direction_en = []
  list_busline_buslist = []
  
  busline_select = "SELECT id, bus_line, bus_start, bus_stop, bus_start_en, bus_stop_en, bus_direction, bus_direction_en, busstop_list FROM busline"

  str_busline_json = str()
  str_stoplist_json = str()

  # find busstop for each busline
  for row in c.execute(busline_select):
    # print(row2[0], row2[1], row2[2], row2[3], row2[4])
    list_busline_id.append(str(row[0]))
    list_busline_number.append(row[1])
    list_busline_start.append(row[2])
    list_busline_stop.append(row[3])
    list_busline_start_en.append(row[4])
    list_busline_stop_en.append(row[5])
    list_busline_direction.append(row[6])
    list_busline_direction_en.append(row[7])
    list_busline_buslist.append(row[8])

  for i in range(len(list_busline_id)):
    # prepare for write json for buslist
    str_busline_json += '"' + list_busline_id[i] + '" :{ '
    str_busline_json += '"busnumber" : "' + list_busline_number[i] + '", '
    str_busline_json += '"busstart" : "' + list_busline_start[i] + '", '
    str_busline_json += '"busstart_en" : "' + list_busline_start_en[i] + '", '
    str_busline_json += '"busstop" : "' + list_busline_stop[i] + '", '
    str_busline_json += '"busstop_en" : "' + list_busline_stop_en[i] + '", '
    str_busline_json += '"direction" : "' + list_busline_direction[i] + '", '
    str_busline_json += '"direction_en" : "' + list_busline_direction_en[i] + '", '
    str_busline_json += '"busstop_list" : ['

    # check query for busstop list
    for row2 in c.execute("SELECT stop_name, stop_name_en, latitude, longitude FROM busstop"):
      # print(row[0], row[1], row[2], row[3], row[4])
      # check if have buslist in json
      if (len(str_stoplist_json) > 0):
        str_stoplist_json += ","
      # prepare for write json for buslist
      str_stoplist_json += '{ "stopname" : "' + row2[0] + '", '
      str_stoplist_json += '  "stopname_en" : "' + row2[1] + '", '
      str_stoplist_json += '  "latitude" : ' + row2[2] + ', '
      str_stoplist_json += '  "longitude" : ' + row2[3] + '" }'

    # prepare for write json for buslist
    str_busline_json += str_stoplist_json
    str_stoplist_json = str()

    str_busline_json += ']'
    str_busline_json += '}'
    
    # not last busline for each busstop
    if (i < len(list_busline_id) - 1):
      str_busline_json += ','

  # write json
  #with open('busline.json', 'w') as outfile:  
  #  json.dump({'"busline" : {" + str_busline_json + "}'}, outfile)

  f = codecs.open('busline.json', 'wb', "UTF-8")
  f.write(u'{"busline" : {" + str_busstop_json + "}}')
  f.close()

  print("Finish Generate sqlite to json : busline")

# play space
if __name__ == '__main__':
  conn = sqlite3.connect('buslinebysukhum.sqlite')
  c = conn.cursor()

  query_busstop(c)
  query_busline(c)
