#!/usr/bin/env python
# coding: utf-8

import xmind
import pandas as pd

#Parameters
_DEFAULT_XLSX_OUTPUT_FILE = "Output.xlsx"

def getSheetList(xbook):
    output={}
    for elt in xbook.getSheets():
        output[elt.getTitle()] = elt
    return output

def getxmindsheetdata(xbook, sheet = ''):
    _data = {}
    if(sheet == ''):
        #Prend le premier onglet
        _data = xbook.getSheets()[0].getData()['topic']
        print('Getting data from first sheet !')
    else:
        #Prend l'onglet sheet
        _data = getSheetList(xbook)[sheet].getData()['topic']
        print('Getting data from '+ sheet +' sheet !')
    
    return _data

def flattenxmind(_dict) :
    """ 
    Xmind data structure to list with path
    
    """
    _list= []
        
    #Iter Function
    def _sub(_subdict, _subparent):
        # First iteration
        if('title' in _subdict.keys()):
            _list.append({
                        'title': _subdict['title'],
                        'note': _subdict['note'],
                        'label': _subdict['note'],
                        'comment': _subdict['comment'],
                        'markers': _subdict['markers'],
                        'parent' : _subparent
                        })
            _updatedparent = _subparent + [_subdict['title']]

            if('topics' in _subdict.keys()):
                if(isinstance(_subdict['topics'],dict)):
                    _sub(_subdict['topics'], _updatedparent)
                elif(isinstance(_subdict['topics'],list)):
                    for elt in _subdict['topics']:
                        _sub(elt, _updatedparent)
    
    # First iteration
    _sub(_dict, [])
    
    return _list
 
def xmindlist2excelformat(_xmindlist):
    _elements = []
    _max_parent = 0
    for line in _xmindlist:
        _destline = [
            line['title'],
            line['note'],
            line['label'],
            line['comment'],
            line['markers'],
            len(line['parent'])
            ] + [_par for _par in line['parent']] +  [line['title']]
        _max_parent = max(_max_parent, len(line['parent']))
        _elements.append(_destline)
    _header = ['title','note', 'label', 'comment', 'markers', 'hierachy'] + ["level " + str(i) for i in range(_max_parent+1)]
    return (_header, _elements)

def xmind2xlsx(xmindfile, sheet='', outputfile =''):
    """ 
    Write Xmind data into a xlsx file formated as a table
    
     Usage : xmind2xls.exe <Xmind File> <flags>
     
     Flags
        -s, --sheet=SHEET : Sheet to read data from
            Default: ''
        -o, --outputfile=OUTPUTFILE : Name of the output file
            Default: ''

    """
    
    _xmind_book = xmind.load(xmindfile)
    print('Reading "' + xmindfile + '" ...')
    #Load xmind data
    _xmind_data = getxmindsheetdata(_xmind_book, sheet)

    #Flatten xmind data in python list
    _flat_xmind = flattenxmind(_xmind_data)

    #Format python list in excel table (business undestanding)
    _xls_data = xmindlist2excelformat(_flat_xmind)

    #Load into a Pandas Dataframe and write it to excel file
    _data = pd.DataFrame(_xls_data[1], columns=_xls_data[0])
    if(outputfile==''):
        _data.to_excel(_DEFAULT_XLSX_OUTPUT_FILE)
        print('File output : ' + _DEFAULT_XLSX_OUTPUT_FILE)
    else:
        _data.to_excel(outputfile)
        print('File output : ' + outputfile)

def __execute():
    import fire
    fire.Fire(xmind2xlsx)

if __name__ == "__main__":
    __execute()