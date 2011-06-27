def string2object(message, data):
    splitteddata = data.split()
    _get_object_from_data(message, splitteddata)

def _get_object_from_data(message, data):
    header_value = []
    tmp_ie_values = []
    tmp_ie_names = []
    #TODO: try to get rid of this reverse
    data.reverse()
    for item in message.items:
        if item == 'Header':
            header_value +=  [data.pop()]
        if item ==  'IE':
            #TODO: create check that tmp_ie_name and expected ie does match
            tmp_ie_names += [data.pop()]
            tmp_ie = [data.pop()]
            tmp_ie_values += tmp_ie
    _check_ies_vs_ies_in_schema(message.ie, tmp_ie_names)
    message.ie = zip(message.ie, tmp_ie_values)
    message.header = zip(message.header, header_value)

def _check_ies_vs_ies_in_schema(ies, tmp_ie_names):
    for i in range(len(ies)):
        tmp_ie = tmp_ie_names[i][:-1]
        if ies[i] != tmp_ie:
            raise Exception("Wrong information element: '"+tmp_ie+"' Expected: '"+ies[i]+"'")