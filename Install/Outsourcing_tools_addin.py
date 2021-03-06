import arcpy
import pythonaddins
import subprocess
import threading
import webbrowser
import functools
import os,re,glob
import arcpy_utils as a
import time,datetime
import logging


class Tools(object):
        
    
    def get_visit_path(self):
        """
        used to find shp from field boundary
        flight and fid are global
        """
        visit_sfile = glob.glob(os.path.join('D:\\Flight ' + str(flight) + '\\field borders\\*{}*.shp'.format(fid)))
        return visit_sfile
    
    def add_layer (self,path):
        """
        add shp file to dataframe
        """
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
        newlayer = arcpy.mapping.Layer(path)
        arcpy.mapping.AddLayer(df, newlayer,"TOP")
        return
        
    
    def save_visit(self,flight_id,fid_id,path = None):
        """
        after save shp to AWS, saved it as visit shp as well
        """
        
        args = ['C:/Users/administrator/Anaconda3/envs/improc/python', 'D:/Program Files/Reg_tool/Install/rezerv_shp.py',str(flight_id),str(fid_id)]
        process = subprocess.Popen(args)
        process.wait()
        if path is not None:
            layer = self.add_layer(path)
        return

    def get_log(self,nameapp,message,infol = None, errorl = None):
        """
        save file with log when user use button
        """
        
        tfolder = os.path.join('C:\\', 'Users', 'Administrator', 'Desktop','Toolbar')# path to save log file 
        if not os.path.exists(tfolder):
            os.makedirs(tfolder)
        now = datetime.datetime.now()
        name = now.strftime("%Y-%m-%d")
        logfile = os.path.join(tfolder,str(name) + '.log')
        logger = logging.getLogger(nameapp)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(logfile)
        formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if infol is not None:
            logger.info(message)
        if errorl is not None:
            logger.error(message)
        
        return 
        

class ButtonClass1(object):
    """
    Process button, used after registretion and saved .txt file
    
    """
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.canRunInBackground = True
        
    def del_pyr(self,path):
        """
        delete pyramid file after transphormation
        """
        pre = os.path.splitext(path)
        lis = glob.glob(pre[0] + '*')
        if len(lis) > 0:
            for file in lis:os.remove(file)
        return 
    
    
    def check_cs(self, imagepath):
        
        new = imagepath.replace('mosaic','registered')
        sc = arcpy.Describe(imagepath).spatialReference
        scnew = arcpy.Describe(new).spatialReference
        path = os.path.split(new)[0]
        name = os.path.split(new)[1]
        if 'rank' in name.lower() and 'jenoptik' in name.lower():
            new = glob.glob(os.path.join('D:\\Flight {}', 'registered', '*{}**{}*.tif').format(str(flight),str(fid),'Jenoptik' ))[0]
            #new = glob.glob(os.path.join(path,'*{}**{}*.tif').format(fid,'Jenoptik')) 
        if 'rank' in name.lower() and 'vnir' in name.lower():  
            new = glob.glob(os.path.join('D:\\Flight {}', 'registered', '*{}**{}*.tif').format(str(flight),str(fid),'VNIR' ))[0]
        if 'rank' in name.lower() and 'ids rgb' in name.lower():  
            new = glob.glob(os.path.join('D:\\Flight {}', 'registered', '*{}**{}*.tif').format(str(flight),str(fid),'IDS RGB'))[0]
        if scnew.name == 'Unknown':
            arcpy.BatchBuildPyramids_management(new)
            arcpy.DefineProjection_management(new, sc)
        else: 
            arcpy.BatchBuildPyramids_management(new)
            #arcpy.MakeRasterLayer_management(new, new)
            arcpy.DefineProjection_management(new, sc)
        pass    
    
    
    def onClick(self):
        
        mxd = arcpy.mapping.MapDocument("CURRENT")  
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        args = ['C:/Users/administrator/Anaconda3/envs/improc/python', 'D:\Program Files\Reg_tool\Install\Registered.py',image]
        print (len(args))
        pre, ext = os.path.splitext(image)
        txt = (pre + '.txt')
        pts = (pre + '.pts')
        if os.path.isfile(txt) == True:
            if os.path.isfile(pts) == True:
                os.remove(pts)
            os.rename(txt,pts)
        self.del_pyr(image.replace('mosaic','registered'))
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        data = process.communicate()
        print (data)
        self.check_cs(image)
        path = os.path.split(image)[0]
        name = os.path.split(image)[1]
        print (name)
        
        """
        if 'jenoptik' not in name.lower():
            jenoptik = glob.glob(os.path.join(path,'*{}**{}*.tif').format(fid,'Jenoptik'))   
            ans = pythonaddins.MessageBox('Use improc.georeference.to_current_vnir(path_tr)', 'Do you want open folder with TR?', 1)
            if ans == 'OK':
                os.startfile(path)
        """

class ButtonClass1(object):
    """
    Process button, used after registretion and saved .txt file
    
    """
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.canRunInBackground = True
                
                
class ButtonClass27(object):
    """
    button for upsync field
    
    """
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.canRunInBackground = True

    def onClick(self):
        message = 'Flight id: {0}, farm id : {1}'.format(flight, fid)
        ans = pythonaddins.MessageBox(message,'Do you want do upsync it ?', 1)
        if ans == 'OK':
            args = ['C:/Users/administrator/Anaconda3/envs/improc/python', 'D:/Program Files/Reg_tool/Install/new_field.py',str(flight),str(fid)]
            process = subprocess.Popen(args)     
            
            
            
class ButtonClass3(object):
    """
    add shp file to dataframe by fid
    """
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.canRunInBackground = True
        
    def onClick(self):
        # fid is global and created when we choose image
        a.add_field(fid)
        pass

class ButtonClass37(object):
    """Implementation for Outsourcing_tools_addin.button_6 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.canRunInBackground = True
        
        
    def syscall(self,call, error_str=None, shell=False):
        """
        Wrapper for very simple call to subprocess to do something on the system
        via python.
        """
    
        try:
            output = subprocess.Popen(
                    call, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE, shell=shell).communicate()[0].decode("utf-8")
        except OSError as e:
            if error_str is not None:
                print(error_str)
            print(e.strerror)
            output = e.strerror
    
        return output

    def run_in_other_thread(self,function): #conflicts w/ os.startfile will crash arcmap.  this is a workaround
    
        # functool.wraps will copy over the docstring and some other metadata
    
        # from the original function
    
        @functools.wraps(function)
    
        def fn_(*args, **kwargs):
    
            thread = threading.Thread(target=function, args=args, kwargs=kwargs)
    
            thread.start()
    
            thread.join()
    
        return fn_



    def shapefile_to_kml(self,shapefilename, kmlfilename=None):
        """
        Converts contents of a shapefile to kml.
    
        Parameters
        ----------
        shapefilename : str
            Full path of shapefile to convert.
        kmlfilename : str
            Full path of kml to be saved.
    
        Returns
        -------
    
        kmlfilename : str
            If exists, full path of output kml.
        """
    
        kmlfilename = kmlfilename or shapefilename.replace('shp', 'kml')
        kmlfilename = os.path.normpath(kmlfilename)
        call = ['ogr2ogr', '-f', 'KML', kmlfilename, shapefilename]
        self.syscall(call)
        startfile = self.run_in_other_thread(os.startfile)
        startfile(kmlfilename)
        #startfile(theFilePath)
        #os.startfile(kmlfilename)
        
        
        #if os.path.isfile(kmlfilename):
            #webbrowser.open(kmlfilename)
            #return kmlfilename
        #else:
            #return None
        
    def onClick(self):
        # fid is global and created when we choose image
        self.shapefile_to_kml(image)
        
        pass

class ButtonClass4(object):
    """
    Button for update to aws
    """
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        get = Tools()
        result = a.update_field_to_aws(fid)
        get.get_log("Updated shp to AWS","For Flight {}, field {}. Result is {} ".format(flight,fid,str(result)), infol = 1)
        visit_sfile = get.get_visit_path()
        if len(visit_sfile) == 0:
            get.save_visit(flight,fid)
            visit_sfile = get.get_visit_path()
        #flight = visit_sfile[1]
        ans = pythonaddins.MessageBox(visit_sfile[0], 'Do you want overwrite this shp', 1)
        if ans == 'OK':
            paths,name = os.path.split(visit_sfile[0])
            #arcpy.env.workspace = paths
            #arcpy.env.overwriteOutput = True
            #arcpy.Delete_management(visit_sfile[0])
            #time.sleep(2)
            farm_layer = "{}_field_boundary".format(fid)
            try:
                get.save_visit(flight,fid,visit_sfile[0])
            except Exception as e:
                get.get_log("Updated shp button","Failed copy shp for Flight {}, field {} the error is : {}. Donwload from database.".format(flight,fid,e), infol = 1)
        pass

class ButtonClass5(object):
    """
    add visit shp for arcgis dataframe 
    """
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        get = Tools()
        visit_sfile = get.get_visit_path()
        if len(visit_sfile) == 0:
            get.save_visit(flight,fid)
            visit_sfile = get.get_visit_path()
        try:
            layer = a.add_shapefile(visit_sfile[0], '{}_visit_boundary'.format(fid))
        except Exception as e:
            get.add_layer(visit_sfile[0])
            print (e)
        pass    
    

class ComboBoxClass2(object):
    """
    Get path to file, name, fid, flight from combobox for script 
    
    
    """
    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWWWWWWWWWWWWW'
        self.width = 'WWWWWWWWWW'
        
        
    def get_fid_from_filename(self, filename):
        fid_regex = re.compile(r"\d\d\d\d-[\d]{1,2}-[\d]{1,2} (?P<fid>[\d]+) ")
        field_ids = fid_regex.findall(filename)
        if field_ids:
            field_id = int(field_ids[0])
            return field_id
        else:
            field_id = int(filename.split(' ')[0])
            return field_id
        raise ValueError("Could not determine field id.")
        
        
    def onSelChange(self, selection):
        
        global image
        global name
        global fid
        global flight
        
        layer = arcpy.mapping.ListLayers(self.mxd, selection)[0]
        
        image = arcpy.Describe(layer).catalogPath
        
        name = arcpy.Describe(image).name
        
        fid = self.get_fid_from_filename(name) 
        
        path = os.path.normpath(image)
        p = path.split(os.sep)
        for i in p:
            if 'Flight' in i:
                flight = int(i[7:])
                break
        pass
    
    
    def onEditChange(self, text):
        self.flight = text
        global fid
        fid = text
        return text
    
    
    def onFocus(self, focused):
        if focused:
            self.mxd = arcpy.mapping.MapDocument('current')
            layers = arcpy.mapping.ListLayers(self.mxd)
            self.items = []
            for layer in layers:
                self.items.append(layer.name)
            """ only for rasters
            for layer in layers:
                if layer.isRasterLayer == True:
                    self.items.append(layer.name)
            """
        pass
    
    
    
    def downsync(self,flight, farm, letter):
        
        args = ["C:/Users/Administrator/Anaconda3/envs/improc/python.exe", 
                "D:/Program Files/Reg_tool/Install/Downsync.py",flight,farm]
        process = subprocess.Popen(args)

 
    def onEnter(self):
        letter = ''
        if len(self.flight) > 0:
            if len(self.flight.split(',')) > 2:
                letter = flight.split(',')[2]
            flight, farm = self.flight.split(',')
            message = 'Flight id: {0}, farm id : {1}'.format(flight, farm)
            ans = pythonaddins.MessageBox(message, 'Do you want downsync this data', 1)
            if ans == 'OK':
                self.downsync(flight, farm, letter)
        pass
    def refresh(self):
        pass


class ButtonClass6(object):
    """
    button for generete product
    
    """
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.canRunInBackground = True

    def onClick(self):
        #begin=time.time()
        message = 'Do you want generate product and upsync - Flight id: {0}, farm id : {1} ?'.format(flight, fid)
        ans = pythonaddins.MessageBox('Click No if you want just generate product and check it before Upsync',message, 3)
        if ans == 'Yes':
            args = ['C:/Users/administrator/Anaconda3/envs/improc/python', 'D:\Program Files\Reg_tool\Install\products.py',str(flight),str(fid),"True"]
            process = subprocess.Popen(args)
        if ans == 'No':
            args = ['C:/Users/administrator/Anaconda3/envs/improc/python', 'D:\Program Files\Reg_tool\Install\products.py',str(flight),str(fid),"False"]
            process = subprocess.Popen(args)
            #process.wait()
            #data = process.communicate()
            #print (data)
            #print(time.time()-begin)
            #"import improc,glob,os;registered_files = glob.glob(os.path.join('D:\\\\','Flight {}','registered','*{}*.tif').format("+str(flight)+","+str(fid)+"))"
            #["C:\Users\Administrator\Anaconda3\envs\improc\python.exe", "-c", "import improc,glob,os;registered_files = glob.glob(os.path.join('D:\\\\', 'Flight {}', 'registered', '*{}*.tif').format("+ str(flight)+","+str(fid)+"));print(type(registered_files));improc.postprocess.generate_products(registered_files)"]
            #cmd = 'C:\\Users\\Administrator\\Anaconda3\\envs\\improc\\python.exe "D:/Program Files/Reg_tool/Install/products.py"'
            #os.system(cmd)
            
    mosaic_block_letter=''
        
    
class Active_Edit_Session(object):
    """
    turn off the oppotuniti to save shp file to aws when editing session is turn on 
    
    """
    def __init__(self):
    # For performance considerations, please remove all unused methods in this class.
        self.enabled = True
    def onStartEditing(self):
        button_2.enabled=False 
    def onStopEditing(self, save_changes):
        button_2.enabled=True
        
