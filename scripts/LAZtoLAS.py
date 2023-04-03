import laspy
import os
import logging

def convert_laz_to_las(in_laz, out_las):
    las = laspy.read(in_laz)
    las = laspy.convert(las)
    las.write(out_las) 

def convert(LAZFolder, OutputFolder):
    try:
        logging.debug('Running LAZ_to_LAS.py')       
        
        in_dir = LAZFolder

        # Loop through all files in the directory  
        for (dirpath, dirnames, filenames) in os.walk(in_dir):
            for inFile in filenames:
                if inFile.endswith('.laz'):	
                    in_laz = os.path.join(dirpath,inFile)
                    
                    out_las = OutputFolder+"/"+inFile
                    out_las = out_las.replace('laz', 'las') 
                    logging.debug(f'working on file: {out_las}')
                    convert_laz_to_las(in_laz, out_las)
                                
        logging.info('Finished without errors - LAZ_to_LAS.py')
    except:
        logging.error('Error in - LAZ_to_LAS.py')