import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy as np
import mplcursors

def wl_to_vel(wl,rest_wl_line):
    zmeas=(wl-rest_wl_line)/rest_wl_line
    vel=(((zmeas+1.0)**2-1.0)*speed_of_light/(1.+(1.+zmeas)**2))
    return vel        

speed_of_light=2.99792e5
rest_wl_si_1=5957.56
rest_wl_si_2=5978.93

#df = pd.read_csv("/Users/umutburgaz/ZTFWork/a_May_28_new/est_5972.csv") umut orignal
df = pd.read_csv(r'C:\Users\senan\OneDrive\Desktop\Capstone\Final_table_allinfo_allcuts.csv')

#spec_phase=df['phase'] umut orignal
#spec_array=df['filename']
#spec_name=df['ztfname']
#redshift=df['redshift']

spec_phase=df['Phase of spectrum']
spec_array=df['Dereddened File Name']
spec_name=df['ztfname']
redshift=df['z']

left_velocities=[]
right_velocities=[]

ahh = 'hello\goodbye'  # just to get the slash in a string
slash = ahh[5] 

for index, row in df.iterrows():
    #print(row['filename'], row['ztfname'], row['phase'], row['redshift']) umut orignal
    print(row['Dereddened File Name'], row['ztfname'], row['Phase of spectrum'], row['z'])
    #spec_file='/Users/umutburgaz/ZTFWork/a_May_28_new/mw_all/'+row['filename'] umut original
    spec_file = r'C:\Users\senan\OneDrive\Desktop\Capstone\dereddend_spectra_and_Si_figures' + slash + row['Dereddened File Name']
    try:
        #data = np.loadtxt(spec_file,dtype={'names': ('wl', 'fl'),'formats': ('f8', 'f8')} ) umut original
        data = pd.read_csv(spec_file)

        #wl_fit1=data['wl']/(1+row['redshift'])             umut original
        #fl_fit1=data['fl']
        #flerr_fit1=data['fl']*0.01
        #velocities = wl_to_vel(wl_fit1, rest_wl_si_1)

        wl_fit1=np.array(data['wl'])/(1+row['z'])
        fl_fit1=np.array(data['fl'])
        flerr_fit1=np.array(data['fl'])*0.01
        velocities = wl_to_vel(wl_fit1, rest_wl_si_1)
    
        mask = np.where((velocities >= -80000) & (velocities <= 40000))
        #y_range = data['fl'][mask]   #umut original
        y_range = np.array(data['fl'])[mask]

        # Define plot and plot data
        fig, ax = plt.subplots()
        #line, = ax.plot(velocities, data['fl'], ':')    umut original
        line, = ax.plot(velocities, np.array(data['fl']), ':')
        ax.set_xlabel("Velocity (km/s)")
        ax.set_ylabel("Flux")
        ax.set_title("Spectrum")
        ax.set_xlim(-50000, 20000)
        ax.axvline(x=-11000, color='r', linestyle='--')
        ax.set_ylim(y_range.min() - y_range.min()*0.1, y_range.max() + y_range.max()*0.1)
        
        vel_left = None
        vel_right = None
        def onclick(event):
            global vel_left, vel_right
            if event.dblclick:
                if vel_left is None:
                    vel_left = event.xdata
                    ax.text(vel_left, 0.9 * ax.get_ylim()[1], f"Vel_left: {vel_left:.2f}", ha='center', va='top', color='red')
                elif vel_right is None:
                    vel_right = event.xdata
                    ax.text(vel_right, 0.9 * ax.get_ylim()[1], f"Vel_right: {vel_right:.2f}", ha='center', va='top', color='red')
                    plt.close()
        
        # Connect event handler to plot to enable interactive/clickable functionality
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        
        # Show the plot
        plt.show()
        
        if vel_left is not None and vel_right is not None:
            print(f"Selected velocity range: [{vel_left:.2f}, {vel_right:.2f}] km/s")
        left_velocities.append(vel_left)
        right_velocities.append(vel_right)
    except FileNotFoundError:
        print(f"File not found: {spec_file}. Skipping...")
    except Exception as e:
        print(f"Error processing file: {spec_file}. Skipping... Error: {str(e)}")
        left_velocities.append(None)
        right_velocities.append(None)  

df1 = pd.DataFrame(spec_array)
df2 = pd.DataFrame(spec_name)
df3 = pd.DataFrame(spec_phase)
df4 = pd.DataFrame(redshift)
df5 = pd.DataFrame(left_velocities)
df6 = pd.DataFrame(right_velocities)

fdf = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
findf = fdf.set_axis(['filename', 'ztfname', 'phase', 'redshift', 'v_x1_5972', 'v_x2_5972'], axis=1)
#findf.to_csv('/Users/umutburgaz/ZTFWork/a_May_28_new/est_5972.csv', index=False)
findf.to_csv('dereddened_files_est_5972.csv')