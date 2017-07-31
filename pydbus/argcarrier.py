'''
Created on July 10, 2017

@author: Harry G. Coin
@copyright: 2017 Quiet Fountain LLC

'''

class ArgCarrier(list,object):
    '''Expesses an argument list as dict, as attrib and list.
    
    Each element of a function call argument list 
    has a value and a numbered position, each keyword element has a name.
    Some elements can have both.
    DBus parameters always have a number and usually have a name.
    This class provides the convenience of being able to refer
    to an argument either way.  If argument in tuple position 2 has name
    'optionB', then ArgCarrier instance a has:
    
    a[2] == a['optionB'] == a.optionB
     
    Setting any of those updates the others.  Set up allows
    defaults and requires parameters arg2pos['name']==offset
    and pos2arg[offset]='name'.  Set up allows any combination
    of initial values in list, dict and default value list form.
    Set up attempts to build a complete list by using
    everything it can from the others, so they can be incomplete
    so long as between them all there is an entry for each
    argument position.
    
    First the instance is set to defaults.  Then it is
    updated with the list form of the arguments, then it is
    updated with the elements in the dictionary.
    
    In the case the name of a dbus argument is a number
    (boo!), or the same as a list attribute (currently
    only '__hash__') use a._name[<dict key>] to force
    lookup by key and not offset.
    
    So, values sent to / returned from Dbus are converted
    to instances of this class.  This is a subclass of
    list, for compatibility with existing dbus code.
        
    '''
    
    class attributes(dict,object):
        def __init__(self,arg2pos,argdict,arglist):
            dict.__init__(argdict)
            self.argdict = argdict
            self.arg2pos=arg2pos
            self.parent_arglist=arglist
            assert isinstance(arg2pos,dict)
            assert len(argdict)==len(arg2pos)
            
        def __getattr__(self,name):
            try:
                return self.argdict[name]
            except:
                pass
            raise AttributeError

        def __setattr__(self,name,value):
            try:
                pos = self.arg2pos[name]
                self.argdict[name]=value
                self.parent_arglist[pos]=value
            except:
                __dict__.__setattr__(name, value)
        
    def _reset_args(self,arglist,argdict):
        '''provide a reset function so users can save set up
        time by re-using instances for the same call/return types.'''
        if (arglist is None) and (argdict is None) and (self.defaults_as_list ==[]):
            raise ValueError("One of arglist or argdict or defaults must not be None")
        if arglist is None: arglist=[]
        if argdict is None: argdict={}
        #Treat any non-list argument as a single argument list
        if not isinstance(arglist,list): arglist = [arglist]
        if not isinstance(argdict,dict):
            raise ValueError("The argument dictionary must be of type dict, not " + str(type(argdict)))
        self.argdict = argdict
        #Use defaults to set missing arguments. Use None to mark spots with no defaults.
        for i in range(len(arglist),len(self.defaults_as_list)):
            arglist += [self.defaults_as_list[i]]
        first_missing_arg_position = len(arglist)
        for i in range(len(arglist),self.argument_positions):
            arglist += [None]

        #First, sync the arglist with anything in the dictionary. 
        for k,v in argdict.items():
            pos = self.argname2position[k]
            if pos>first_missing_arg_position:
                first_missing_arg_position=pos
            arglist[pos]=v
        #check for members with a name but no value and no default
        if first_missing_arg_position != self.argument_positions:
            raise ValueError("Expected a total of " + str(self.argument_positions)+ " but detected "+str(first_missing_arg_position+1))
        #Next, sync the dictionary with anything in the arglist
        for i in range(0,len(arglist)):
            argdict[self.position2argname[i]]=arglist[i]
                
        #Set instance up to function as list
        list.__init__(self,arglist)
        #Set extension up to function as access via dict and/or attributes
        #self.args = self.attributes(arg2pos,self.argdict,self)


    def __init__(self,argnames,defaults=None,arglist=None,argdict=None):
                
        if defaults is None: defaults = []
        self.defaults_as_list = defaults
        if isinstance(argnames,list):
            self.position2argname = argnames
        elif isinstance(argnames,dict):
            if len(argnames)>0:
                self.position2argname=[]
                self.position2argname = [ "!!!" for i in range(0,len(argnames)) ]
                for k,v in argnames.items():
                    if isinstance(k,int):
                        if self.position2argname[k] != "!!!":
                            raise ValueError("Position "+str(k)+" appears twice in argname doct")
                        self.position2argname[k]=v
                    else:
                        if self.position2argname[v] != "!!!":
                            raise ValueError("Position "+str(v)+" appears twice in argname dict")
                        self.position2argname[v]=k
        else:
            raise ValueError("argnames must be either a list or a dictionary of name:positions or position:names")
        self.argname2position = {}
        try:
            for i in range(0,len(self.position2argname)):
                name = self.position2argname[i]
                if not isinstance(name,str):
                    raise ValueError("All argument position names must be strings, not: "+str(name))
                self.argname2position[name]=i
        except:
            raise ValueError("Could not reference all the elements in the arglist: "+str(self.position2argname))

        self.argument_positions = len(self.position2argname)
            
        if self.argument_positions <1:
            raise ValueError("There must be at least one name/argument position.")
        
        
        if (arglist is not None) or (argdict is not None): self._reset_args(arglist,argdict)
        #Fill arglist with any missing defaults, or None if no defaults
        
     
    def __getitem__(self,key):
        '''override list to allow x['name'] dict behavior when key is not an int'''
        try:
            if isinstance(key,int):
                return list.__getitem__(self,key)
        except:
            if key in self.argdict: return self.argdict[key]
            raise
        return self.argdict[key]

    def __setitem__(self,key,value):
        '''override to allow x['name'] dict behavior when key is not an int'''
        if isinstance(key,int): 
            list.__setitem__(self,key,value)
            self.argdict[self.position2argname[key]]=value
        else:
            if key in self.argname2position: 
                key_pos = self.argname2position[key]
                self.argdict[key]=value
                list.__setitem__(self,key_pos,value)
            else:
                raise

    def __getattr__(self,name):
        try:
            return list.__getattr__(self,name)
        except:
            pass
        try:
            return object.__getattr__(self,name)
        except:
            pass
        try:
            d = object.__getattribute__(self,'argdict')
            return d[name]
        except:
            pass
        raise AttributeError("Attribute "+str(name)+" not found in ArgCarrier instance.")

    def __setattr__(self,name,value):
        '''even though it's a list, treat as dict if key in dict'''
        try:
            pos = self.argname2position[name]
            #Only set known names, no other attributes allowed.
            self.argdict[name]=value
            self[pos]=value
            return
        except:
            pass
        if hasattr(list,name):
            list.__setattr__(self,name, value)
            return
        object.__setattr__(self,name,value)
                
    
if __name__ == "__main__":    
    a = ArgCarrier(argnames=['a','b','c'],arglist=['zero','overwritten'],argdict={'b':'one'},defaults=['not','seen','seeme'])
    print(a['a'])
    print(a[1])
    print(a['c'])
    print(str(a))
    a[1]="WON!"
    print(a.b)
    a.b="Double Win!"
    print(a[1])
    a['b']="Trifecta!"
    print(a[1])
    a = ArgCarrier(argnames={'a':0,'b':1,'c':2},arglist=['zero','overwritten'],argdict={'b':'one'},defaults=['not','seen','seeme'])
    print(a['a'])
    print(a[1])
    print(a['c'])
    a = ArgCarrier(argnames={0:'a',1:'b',2:'c'},arglist=['zero','overwritten'],argdict={'b':'one'},defaults=['not','seen','seeme'])
    print(a['a'])
    print(a[1])
    print(a['c'])

        