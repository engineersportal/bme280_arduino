# Calculating radius and gravity at latitude point
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

x_var = np.arange(0,90,.1)
r_0,g_phi = [],[]
for lat in x_var:
    phi = lat*(np.pi/180)
    a = 6378137.0
    b = 6356752.3141
    g_e = 9.7803267715
    g_p = 9.8321863685
    k = ((b*g_p)/(a*g_e))-1.0
    e_c = ((a**2.0)-(b**2.0))/(a**2.0)

    r_0.append(np.sqrt(((((a**2.0)*np.cos(phi))**2.0)+(((b**2.0)*np.sin(phi))**2.0))/
                  (((a*np.cos(phi))**2.0)+((b*np.sin(phi))**2.0))))

    ##phi = np.arctan(((1-e_c))*np.tan(phi))
    g_phi.append(g_e*((1+(k*((np.sin(phi))**2.0)))/
                 (np.sqrt(1-((e_c)*(np.sin(phi)**2.0))))))

    g_phi_1980 = 9.780327*(1 + (0.0053024*(np.power(np.sin(phi),2.0))-(0.0000058*(np.power(np.sin(2.0*phi),2.0)))))

##print('At Lat: {0:2.2f} -> r_0 = {1:2.5f}'.format(phi,r_0))
##print('g (Somigliana) = {0:2.5f}, g (1980) = {1:2.5f}'.format(g_phi,g_phi_1980))

r_0 = np.divide(r_0,1000.0)
# plotting routing

fig = plt.figure(figsize=(14,8))
ax1 = fig.add_subplot(111)
p1, = ax1.plot(x_var,r_0,label='Radius',linewidth=5,color='#962045') # scatter plot
ax2 = ax1.twinx()
p2, = ax2.plot(x_var,g_phi,label='Gravitational Acceleration',
         linewidth=5,color='#469620') # line plot with average
subplot_vec = [p1,p2]
ax2.legend(subplot_vec,[l.get_label() for l in subplot_vec],fontsize=20,loc='upper center')
ax1.yaxis.label.set_color(p1.get_color())
ax2.yaxis.label.set_color(p2.get_color())
ax2.grid(False)
ax1.spines["right"].set_edgecolor(p1.get_color())
ax2.spines["right"].set_edgecolor(p2.get_color())
ax1.tick_params(axis='y', colors=p1.get_color())
ax2.tick_params(axis='y', colors=p2.get_color())
# styling the plot with labels, limits, and legend
ax1.set_ylabel('Radius [km]',fontsize=20)
ax2.set_ylabel(r'Acceleration [m/s$^2$]',fontsize=20)
plt.xlim([0.0,90.0])
ax1.set_xlabel('Geodetic Latitude',fontsize=20)
##plt.legend(fontsize=16)
plt.savefig('radius_gravity_latitude.png',dpi=200)
plt.show()
