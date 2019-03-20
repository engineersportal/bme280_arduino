# Calculating radius and gravity at latitude point
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

# earth's radius and gravitational acceleration calculation section
lat = 40.7128 # input lat
phi = lat*(np.pi/180)
a = 6378137.0 # radius at equator
b = 6356752.3141 # radius at pole
g_e = 9.7803267715 # gravity at equator
g_p = 9.8321863685 # gravity at pole
k = ((b*g_p)/(a*g_e))-1.0 # normal gravity constant 
e_c = ((a**2.0)-(b**2.0))/(a**2.0) # earth eccentricity

r_0 = (np.sqrt(((((a**2.0)*np.cos(phi))**2.0)+(((b**2.0)*np.sin(phi))**2.0))/
              (((a*np.cos(phi))**2.0)+((b*np.sin(phi))**2.0))))

g_phi = (g_e*((1+(k*((np.sin(phi))**2.0)))/
             (np.sqrt(1-((e_c)*(np.sin(phi)**2.0))))))

##g_phi_1980 = 9.780327*(1 + (0.0053024*(np.power(np.sin(phi),2.0))-(0.0000058*(np.power(np.sin(2.0*phi),2.0)))))

# calculation of density

p_0 = 1013.2 # measured pressure at sea level (from NOAA)
p_0 = p_0*100.0
h = 0.5 # measured relative humidity (from NOAA)
T = 50.0 # measured temperature in F
T = (T-32.0)*(5.0/9.0)+273.15 # temp in Kelvin
R_d = 287.058 # dry air specific gas constant
R_v = 461.495 # water vapor specific gas constant

p_sat = 0.61121*np.exp((18.678-(T/234.5))*(T/(257.14+T)))

rho = (p_0/(R_d*T))+((h*p_sat)/(R_v*T))

# calculation of altitude using pressure measurement

q = 1.4 # assumption: polytropic index is equal to ratio of specific heats

T_lapse = 0.0065# temperature lapse rate for isothermal atmosphere

p_range = np.arange(1500.0,500.0,-0.1)
q_range = np.arange(0.4,2.0,0.2)
q_range = np.delete(q_range,np.argmin(np.abs(np.subtract(q_range,1.0))))
fig = plt.figure(figsize=(14,8))
for q in q_range:
    z,z_taylor,z_isotherm,z_standard = [],[],[],[]
    for pres in p_range:
    ##p_meas = 1019.85
        p_meas = pres*100.0
        A = p_0/(rho*g_phi*r_0*(1-q))
        z.append(r_0*((np.power(((A*((np.power(p_meas/p_0,1-q))-1.0)))+1.0,-1.0))-1.0))

        # Taylor series comparison
        z_taylor.append((p_0/(rho*g_phi*(1.0-q)))*(1.0-(np.power(p_meas/p_0,1.0-q))))

        # isothermal assumption
        z_isotherm.append(-1.0*((p_0/(rho*g_phi))*np.log(p_meas/p_0)))

        z_standard.append((((np.power(p_0/p_meas,(p_0*T_lapse)/(rho*T*g_phi)))*T)-T)/T_lapse)
##    plt.plot(p_range,z,label='q = {0:2.2f} Exact'.format(q),linewidth=5,linestyle='--')
    if round(q,2)==1.4:
        plt.plot(p_range,z_taylor,label='q = {0:2.2f} (Adiabat)'.format(q),linewidth=3)
    else:
        plt.plot(p_range,z_taylor,label='q = {0:2.2f}'.format(q),linewidth=3)

print('Mean Absolute Difference: {0:2.2f}'.format(np.mean(np.abs(np.subtract(z,z_taylor)))))
plt.plot(p_range,z_standard,label='lapse rate',linewidth=3,linestyle='--')
plt.plot(p_range,z_isotherm,label='q = 1.00 (Isotherm)',linestyle=':',linewidth=3)
plt.ylim([0.0,1500.0])
plt.xlim([850.0,1013.0])
plt.xlabel('Pressure Measurement [hPa]',fontsize=20)
plt.ylabel('Altitude [m]',fontsize=20)
plt.legend(fontsize=16)
ax1 = plt.gca()
ax1.axes.tick_params(axis='both',labelsize=16,pad=5)
plt.tight_layout(pad=1.4)
plt.savefig('altitude_adiabat_isotherm.png',dpi=200)

plt.show()

# analyzing the isothermal, adiabatic, and lapse rate profiles
fig = plt.figure(figsize=(14,8))
p_range = np.arange(1013.0,700.0,-0.1)
z,z_taylor,z_isotherm,z_standard = [],[],[],[]
q = 1.2
for pres in p_range:
##p_meas = 1019.85
    p_meas = pres*100.0
    A = p_0/(rho*g_phi*r_0*(1-q))
    z.append(r_0*((np.power(((A*((np.power(p_meas/p_0,1-q))-1.0)))+1.0,-1.0))-1.0))

    # Taylor series comparison
    z_taylor.append((p_0/(rho*g_phi*(1.0-q)))*(1.0-(np.power(p_meas/p_0,1.0-q))))

    # isothermal assumption
    z_isotherm.append(-1.0*((p_0/(rho*g_phi))*np.log(p_meas/p_0)))

    z_standard.append((((np.power(p_0/p_meas,(p_0*T_lapse)/(rho*T*g_phi)))*T)-T)/T_lapse)
##    plt.plot(p_range,z,label='q = {0:2.2f} Exact'.format(q),linewidth=5,linestyle='--')

plt.plot(p_range,z_taylor,label='q = {0:2.2f}'.format(q),linewidth=3)

print('MAE Z-Taylor and Z-Lapse: {0:2.2f}'.format(np.mean(np.abs(np.subtract(z_taylor,z_standard)))))
print('MAE Z-isotherm and Z-Lapse: {0:2.2f}'.format(np.mean(np.abs(np.subtract(z_standard,z_isotherm)))))

plt.plot(p_range,z_standard,label='Lapse Rate = -0.0065',linewidth=3,linestyle='--')
plt.plot(p_range,z_isotherm,label='q = 1.00 (Isotherm)',linestyle=':',linewidth=3)
##plt.ylim([0.0,1500.0])
##plt.xlim([850.0,1013.0])
plt.xlabel('Pressure Measurement [hPa]',fontsize=20)
plt.ylabel('Altitude [m]',fontsize=20)
plt.legend(fontsize=16)
ax1 = plt.gca()
ax1.axes.tick_params(axis='both',labelsize=16,pad=5)
plt.tight_layout(pad=1.4)

err_pts = 4
for ii in range(0,err_pts):
    err_range = p_range[ii*int(len(z_standard)/err_pts):(ii+1)*int(len(z_standard)/err_pts)]
    taylor_range = z_taylor[ii*int(len(z_standard)/err_pts):(ii+1)*int(len(z_standard)/err_pts)]
    lapse_range = z_standard[ii*int(len(z_standard)/err_pts):(ii+1)*int(len(z_standard)/err_pts)]
    iso_range = z_isotherm[ii*int(len(z_standard)/err_pts):(ii+1)*int(len(z_standard)/err_pts)]

    midpoint = int((((ii+1)*int(len(z_standard)/err_pts))-(ii*int(len(z_standard)/err_pts)))/2.0)
    # error at specific points
    mae_iso = np.sqrt(np.mean(np.power(np.subtract(iso_range,lapse_range),2.0)))
    mae_adiabat = np.sqrt(np.mean(np.power(np.subtract(taylor_range,lapse_range),2.0)))
    ax1.annotate('Lapse-Isotherm Error: {0:2.1f} m\nLapse-Near Adiabat Error: {1:2.1f} m'.format(mae_iso,mae_adiabat),
                 xy=(err_range[midpoint],iso_range[midpoint]), xytext=(0.0, -65),
                 textcoords = 'offset points',ha='center',
                arrowprops=dict(facecolor='black', shrink=0.05),
                )

plt.savefig('lapse_adiabat_isotherm_err.png',dpi=200)

plt.show()
