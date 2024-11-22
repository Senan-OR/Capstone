import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy as np
import mplcursors
from os import listdir
from extinction import ccm89, apply, remove
  

speed_of_light=2.99792e5
rest_wl_Ti=4301.914

#df = pd.read_csv(r'C:\Users\senan\OneDrive\Desktop\Capstone\csv_files\Master_info.csv')        for the ztf files

#phases=df['Phase of spectrum']
#files=df['Dereddened File Name']
#names=df['ztfname']
#zs=df['z']
#snr=df['SNR']

#spec_phase=[]
#spec_array=[]
#spec_name=[]
#redshift=[]
#snr_cut=[]

#for i in range(len(names)):
#    if snr[i] >=4:
#        spec_phase.append(phases[i])
#        spec_array.append(files[i])
#        spec_name.append(names[i])
#        redshift.append(zs[i])
#        snr_cut.append(snr[i])

#spec_phase = np.array(spec_phase)
#spec_array = np.array(spec_array)
#spec_name = np.array(spec_name)
#redshift = np.array(redshift)
#snr_cut = np.array(snr_cut)


#df1 = pd.DataFrame(spec_array)
#df2 = pd.DataFrame(spec_name)
#df3 = pd.DataFrame(spec_phase)
#df4 = pd.DataFrame(redshift)
#df5 = pd.DataFrame(snr_cut)

#fdf = pd.concat([df1, df2, df3, df4, df5], axis=1)
#findf = fdf.set_axis(['Dereddened File Name', 'ztfname', 'Phase of spectrum', 'z', 'SNR'], axis=1)

wavelength_min = 3900
wavelength_max = 4500
ahh = 'hello\goodbye'
slash = ahh[5]

#path = r'C:\Users\senan\OneDrive\Desktop\Capstone\subtype_files\11fe'
#z = 0.000804
#mwebv = 0.0077
#path = r'C:\Users\senan\OneDrive\Desktop\Capstone\subtype_files\86G'
#z = 0.007735
#mwebv = 0.1155
path = r'C:\Users\senan\OneDrive\Desktop\Capstone\subtype_files\91bg'
z = 0.015
mwebv = 0.1245 

allfiles = listdir(path)

#allfiles_wlcut = []
#for i in range(len(allfiles)):                                                        #removes the files that arent in the wavelength range
#    if allfiles[i][-4:-1] == '.cs':
#        data=pd.read_csv(path + slash + allfiles[i])
#    else:
#        data=pd.read_csv(path + slash + allfiles[i], delim_whitespace=True)
#    wl = np.array(data['wl']) / (1+z)
#    if wl[0] > wavelength_min - 100:
#        allfiles_wlcut.append(allfiles[i])

left_wavelengths=[]
right_wavelengths=[]

#for index, row in findf.iterrows():    for the ztf files
#    print(row['Dereddened File Name'], row['ztfname'], row['Phase of spectrum'], row['z'])
#    spec_file = r'C:\Users\senan\OneDrive\Desktop\Capstone\dereddened_spectra' + slash + row['Dereddened File Name']
#    try:
#        data = pd.read_csv(spec_file)

for i in range(len(allfiles)):
    spec_file = path + slash + allfiles[i]
    try:
        if allfiles[i][-4:-1] == '.cs':
            data=pd.read_csv(path + slash + allfiles[i])
        else:
            data=pd.read_csv(path + slash + allfiles[i], delim_whitespace=True)

        #wl_fit1=np.array(data['wl'])/(1+row['z'])
        wl_fit1=np.array(data['wl'])
        waveno = 1/(wl_fit1 * 1e-4) 
        wl_fit1 = wl_fit1 / (1+z)
        fl=np.array(data['fl'])
        flerr=np.array(data['fl'])*0.01
        R_v = 3.1
        A_v = R_v * mwebv
        fl_fit1 = remove(ccm89(waveno, A_v, R_v, unit='invum'), fl)
        

        #if min(wl_fit1) < 3000:
        #    mask = np.where((wl_fit1 >= 3000) & (wl_fit1 <=5000))          #apply this bit if to look at the Ti feature
        #else:
        #    mask = np.where((wl_fit1 >= min(wl_fit1)) & (wl_fit1 <=5000))
        #y_range = np.array(data['fl'])[mask]

        # Define plot and plot data
        fig, ax = plt.subplots()
        line, = ax.plot(wl_fit1, np.array(data['fl']), ':')#, label=row['SNR'])
        ax.set_xlabel("Wavelength ($\AA$)")
        ax.set_ylabel("Flux")
        #ax.set_title(row['ztfname'])
        ax.set_title(allfiles[i])
        ax.legend()
        
        ###ax.set_xlim(-50000, 20000)

        if min(wl_fit1) < 3000:                #apply this bit if to look at the Ti feature
            ax.set_xlim(3000,5000)
        else:
            ax.set_xlim(min(wl_fit1),5000)
        #ax.set_xlim(6000,7000)

        ax.axvline(x=rest_wl_Ti, color='r', linestyle='--')
        #ax.axvline(x=7000, color='r', linestyle='--')
        ax.axvline(x=3863.703677253942, color='k', linestyle='--')
        ax.axvline(x=4472.433850153616, color='k', linestyle='--')
        #ax.set_ylim(y_range.min() - y_range.min()*0.1, y_range.max() + y_range.max()*0.1) #apply this bit if to look at the Ti feature
        
        wl_left = None
        wl_right = None
        def onclick(event):
            global wl_left, wl_right
            if event.dblclick:
                if wl_left is None:
                    wl_left = event.xdata
                    ax.text(wl_left, 0.9 * ax.get_ylim()[1], f"wl_left: {wl_left:.2f}", ha='center', va='top', color='red')
                elif wl_right is None:
                    wl_right = event.xdata
                    ax.text(wl_right, 0.9 * ax.get_ylim()[1], f"wl_right: {wl_right:.2f}", ha='center', va='top', color='red')
                    plt.close()
        
        # Connect event handler to plot to enable interactive/clickable functionality
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        
        # Show the plot
        plt.show()
        
        if wl_left is not None and wl_right is not None:
            print(f"Selected wavelength range: [{wl_left:.2f}, {wl_right:.2f}] $\AA$")
        left_wavelengths.append(wl_left)
        right_wavelengths.append(wl_right)
    except FileNotFoundError:
        print(f"File not found: {spec_file}. Skipping...")
    except Exception as e:
        print(f"Error processing file: {spec_file}. Skipping... Error: {str(e)}")
        left_wavelengths.append(None)
        right_wavelengths.append(None)  

#findf.insert(4, 'wl_x2_Ti', right_wavelengths, True)
#findf.insert(4, 'wl_x1_Ti', left_wavelengths, True)

df1 = pd.DataFrame(allfiles)
df2 = pd.DataFrame(left_wavelengths)
df3 = pd.DataFrame(right_wavelengths)
fdf = pd.concat([df1, df2, df3], axis=1)
findf = fdf.set_axis(['File Name', 'wl_x1_Ti', 'wl_x2_Ti'], axis=1)
findf.to_csv(r'C:\Users\senan\OneDrive\Desktop\Capstone\subtype_files\91bg_clicks_new.csv')