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
rest_wl_si_1=6347.103
rest_wl_si_2=6371.359

df = pd.read_csv("/Users/umutburgaz/ZTFWork/a_May_28_new/new_ones_to_fit.csv")

spec_phase=df['phase']
spec_array=df['filename']
spec_name=df['ztfname']
redshift=df['redshift']

left_velocities=[]
right_velocities=[]

for index, row in df.iterrows():
    print(row['filename'], row['ztfname'], row['phase'], row['redshift'])
    spec_file='/Users/umutburgaz/ZTFWork/a_May_28_new/mw_all/'+row['filename']
    try:
        data = np.loadtxt(spec_file,dtype={'names': ('wl', 'fl'),'formats': ('f8', 'f8')} )
        wl_fit1=data['wl']/(1+row['redshift'])
        fl_fit1=data['fl']
        flerr_fit1=data['fl']*0.01
        velocities = wl_to_vel(wl_fit1, rest_wl_si_1)
    
        mask = np.where((velocities >= -80000) & (velocities <= 40000))
        y_range = data['fl'][mask]
        
        fig, ax = plt.subplots()
        line, = ax.plot(velocities, data['fl'], ':')
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
        
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        
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
findf = fdf.set_axis(['filename', 'ztfname', 'phase', 'redshift', 'v_x1_6355', 'v_x2_6355'], axis=1, inplace=False)
findf.to_csv('/Users/umutburgaz/ZTFWork/a_May_28_new/fit_6355.csv', index=False)