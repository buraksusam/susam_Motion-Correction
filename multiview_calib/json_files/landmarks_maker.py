import json

f = open('results/result_6_1.json')
data = json.load(f)
ids = [*range(0,17)]
ids.remove(3)
ids.remove(4)

dict_list = []
landmark_dict = {}

for i in range(len(data["Info"])): #buraya videodaki frame range'i gelecek
    landmark_dict["6_1"] = {}
    landmark_dict["6_1"]["landmarks"] = []
    landmark_dict["6_1"]["ids"] = ids
    if data["Info"][i]["keypoints"] != None:
        for j in range(len(data["Info"][i]["keypoints"])):
            if j == 3 or j == 4:
                j += 1
            else:
                tmp_list = []
                tmp_list.append(data["Info"][i]["keypoints"][j][0])
                tmp_list.append(data["Info"][i]["keypoints"][j][1])
                landmark_dict["6_1"]["landmarks"].append(tmp_list)
        tmp = landmark_dict.copy() 
        dict_list.append(tmp)
    else:
        tmp = landmark_dict.copy() 
        dict_list.append(tmp)


#6_2 nin jsonu okuyup dicte çevir
f = open('results/result_6_2.json')
data = json.load(f)

for i in range(len(data["Info"])): #buraya videodaki frame range'i gelecek
    if i <= len(dict_list) - 1:
        landmark_dict = dict_list[i]
    else:
        landmark_dict = dict_list[0]
    landmark_dict["6_2"] = {}
    landmark_dict["6_2"]["landmarks"] = []
    landmark_dict["6_2"]["ids"] = ids
    if data["Info"][i]["keypoints"] != None:
        for j in range(len(data["Info"][i]["keypoints"])):
            if j == 3 or j == 4:
                j += 1
            else:
                tmp_list = []
                tmp_list.append(data["Info"][i]["keypoints"][j][0])
                tmp_list.append(data["Info"][i]["keypoints"][j][1])
                landmark_dict["6_2"]["landmarks"].append(tmp_list)
    else:
        tmp = landmark_dict.copy()
        dict_list[i] = tmp
    if i < len(data["Info"]) - 1:
        tmp = landmark_dict.copy()
        dict_list[i] = tmp
    else:
        tmp = landmark_dict.copy()
        dict_list.append(tmp)

#6_3 nin jsonu okuyup dicte çevir
f = open('results/result_6_3.json')
data = json.load(f)

for i in range(len(data["Info"])): #buraya videodaki frame range'i gelecek
    if i <= len(dict_list) - 1:
        landmark_dict = dict_list[i]
    else:
        landmark_dict = dict_list[0]
    landmark_dict["6_3"] = {}
    landmark_dict["6_3"]["landmarks"] = []
    landmark_dict["6_3"]["ids"] = ids
    if data["Info"][i]["keypoints"] != None:
        for j in range(len(data["Info"][i]["keypoints"])):
            if j == 3 or j == 4:
                j += 1
            else:
                tmp_list = []
                tmp_list.append(data["Info"][i]["keypoints"][j][0])
                tmp_list.append(data["Info"][i]["keypoints"][j][1])
                landmark_dict["6_3"]["landmarks"].append(tmp_list)
    else:
        tmp = landmark_dict.copy()
        dict_list[i] = tmp
    if i <= len(dict_list) - 1:
        tmp = landmark_dict.copy()
        dict_list[i] = tmp
    else:
        tmp = landmark_dict.copy()
        dict_list.append(tmp)

#6_4 nin jsonu okuyup dicte çevir
f = open('results/result_6_4.json')
data = json.load(f)

for i in range(len(data["Info"])): #buraya videodaki frame range'i gelecek
    if i <= len(dict_list) - 1:
        landmark_dict = dict_list[i]
    else:
        landmark_dict = dict_list[0]
    landmark_dict["6_4"] = {}
    landmark_dict["6_4"]["landmarks"] = []
    landmark_dict["6_4"]["ids"] = ids
    if data["Info"][i]["keypoints"] != None:
        for j in range(len(data["Info"][i]["keypoints"])):
            if j == 3 or j == 4:
                j += 1
            else:
                tmp_list = []
                tmp_list.append(data["Info"][i]["keypoints"][j][0])
                tmp_list.append(data["Info"][i]["keypoints"][j][1])
                landmark_dict["6_4"]["landmarks"].append(tmp_list)
    else:
        tmp = landmark_dict.copy()
        dict_list[i] = tmp
    if i <= len(dict_list) - 1:
        tmp = landmark_dict.copy()
        dict_list[i] = tmp
    else:
        tmp = landmark_dict.copy()
        dict_list.append(tmp)

#6_5 nin jsonu okuyup dicte çevir
f = open('results/result_6_5.json')
data = json.load(f)

for i in range(len(data["Info"])): #buraya videodaki frame range'i gelecek
    if i <= len(dict_list) - 1:
        landmark_dict = dict_list[i]
    else:
        landmark_dict = dict_list[0]
    landmark_dict["6_5"] = {}
    landmark_dict["6_5"]["landmarks"] = []
    landmark_dict["6_5"]["ids"] = ids
    if data["Info"][i]["keypoints"] != None:
        for j in range(len(data["Info"][i]["keypoints"])):
            if j == 3 or j == 4:
                j += 1
            else:
                tmp_list = []
                tmp_list.append(data["Info"][i]["keypoints"][j][0])
                tmp_list.append(data["Info"][i]["keypoints"][j][1])
                landmark_dict["6_5"]["landmarks"].append(tmp_list)
    else:
        tmp = landmark_dict.copy()
        dict_list[i] = tmp
    if i <= len(dict_list) - 1:
        tmp = landmark_dict.copy()
        dict_list[i] = tmp
    else:
        tmp = landmark_dict.copy()
        dict_list.append(tmp)

import os.path

for i in range(len(dict_list)):
    jsonString = json.dumps(dict_list[i])
    file_name = "landmarks_frame_"+str(i)+".json"
    save_path = "/cvlabdata2/home/susam/Motion-Correction/multiview_calib/json_files/landmarks"
    complete_name = os.path.join(save_path, file_name)
    jsonFile = open(complete_name, "w")
    jsonFile.write(jsonString)
    jsonFile.close()