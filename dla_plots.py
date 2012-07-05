# vim: set fileencoding=utf-8
"""
This is a module for making plots like those in Tescari & Viel, based on the data gathered in the Halohi module
Figures implemented:
    5,6,9,10-13
Possible but not implemented:
    14
        """

import halohi
import numpy as np
import os.path as path
import math
import matplotlib.pyplot as plt

acol="blue"
gcol="red"
acol2="cyan"
gcol2="magenta"
rcol="black"
astyle="-"
gstyle="--"

#These are parameters for the analytic fits for the DLA abundances.
#Format: a,b,ra,rb
#breakpoint is at 10^10.5
#arepo_halo_p = {
#                90 : [  2.51567291,  32.66547647,  67.72689814],
#                91 : [  2.51567291,  32.66547647,  67.72689814],
#                124 : [  2.60395335,  32.53670302,  55.67506455],
#                141 :  [  2.82049202,  32.3547484,   38.4643012 ],
#                191 : [  3.35225558,  31.33131514,  -3.12604689],
#                314 :  [  2.94558432,  28.65151923,   5.38257005]
#                }
#
#gadget_halo_p = {
#                   90 :  [  2.5118343, 33.16836309,  50.20590397],
#                   91 :  [  2.5118343, 33.16836309,  50.20590397],
#                  124 :  [  3.14882076,  32.56825392,  -7.62043225],
#                  141 :  [  3.53242792,  32.23375728, -25.709872  ],
#                  191 : [  4.2523147,   30.89908674, -38.59637455],
#                  314 : [  3.04860987,  28.39565676,   0.37187526]
#                  }
arepo_halo_p = {
90  : [ 0.474492395744 , 32.3354193529 , 64.1103696034 , 1025.39160514 , 1.92971408154 , ],
124  : [ 0.487794225616 , 32.4859370217 , 60.2350857347 , 4.20000415528 , 6.13774174794 , ],
141  : [ 0.544063343988 , 32.3207571363 , 40.5794243679 , 4.475671217 , 4.72298619854 , ],
191  : [ 0.527333697086 , 32.3853042367 , 32.6371468335 , -1014.98380623 , 0.798750441217 , ],
314  : [ 0.439603148064 , 29.6906451591 , 17.6915078157 , -988.969576462 , 0.539761427411 , ],
}
gadget_halo_p = {
90  : [ 0.402940063958 , 32.6466010088 , 48.0841552686 , 1025.30584919 , 3.33453531055 , ],
124  : [ 0.494941169663 , 32.0953160165 , -3.49968288156 , 570.134065046 , 3.20262281821 , ],
141  : [ 0.579598438527 , 31.8871826025 , -20.3179751964 , 310.979609542 , 3.00516724233 , ],
191  : [ 0.789194644499 , 30.8217753689 , -36.2936679845 , 39.9854892473 , 2.61812985859 , ],
314  : [ 0.601313193827 , 28.4976541793 , 0.929240785596 , -171.650139315 , 0.872400813277 , ],
}


def pr_num(num,rnd=2):
    """Return a string rep of a number"""
    return str(np.round(num,rnd))


class PrettyHalo(halohi.HaloHI):
    """
    Derived class with extra methods for plotting a pretty (high-resolution) picture of the grid around a halo.
    """

    def plot_pretty_something(self,num,grid,bar_label):
        """
        Plots a pretty (high-resolution) picture of the grid around a halo.
        Helper for the other functions.
        """
        #Plot a figure
        vmax=np.max([np.max(grid),25.5])
        maxdist = self.sub_radii[num]
        plt.imshow(grid,origin='lower',extent=(-maxdist,maxdist,-maxdist,maxdist),vmin=0,vmax=vmax)
        bar=plt.colorbar(use_gridspec=True)
        bar.set_label(bar_label)
        if (maxdist > 150) * (maxdist < 200):
            plt.xticks((-150,-75,0,75,150))
            plt.yticks((-150,-75,0,75,150))
        if maxdist > 300:
            plt.xticks((-300,-150,0,150,300))
            plt.yticks((-300,-150,0,150,300))
        plt.xlabel(r"x (kpc h$^{-1}$)")
        plt.ylabel(r"y (kpc h$^{-1}$)")
        plt.tight_layout()
        plt.show()

    def plot_pretty_halo(self,num=0):
        """
        Plots a pretty (high-resolution) picture of the grid around a halo.
        """
        self.plot_pretty_something(num,self.sub_nHI_grid[num],"log$_{10}$ N$_{HI}$ (cm$^{-2}$)")

    def plot_pretty_cut_halo(self,num=0,cut_LLS=17,cut_DLA=20.3):
        """
        Plots a pretty (high-resolution) picture of the grid around a halo.
        """
        cut_grid=np.array(self.sub_nHI_grid[num])
        ind=np.where(cut_grid < cut_LLS)
        cut_grid[ind]=10
        ind2=np.where((cut_grid < cut_DLA)*(cut_grid > cut_LLS))
        cut_grid[ind2]=17.
        ind3=np.where(cut_grid > cut_DLA)
        cut_grid[ind3]=20.3
        maxdist = self.sub_radii[num]
        plt.imshow(cut_grid,origin='lower',extent=(-maxdist,maxdist,-maxdist,maxdist),vmin=10,vmax=20.3)
        if (maxdist > 150) * (maxdist < 200):
            plt.xticks((-150,-75,0,75,150))
            plt.yticks((-150,-75,0,75,150))
        if maxdist > 300:
            plt.xticks((-300,-150,0,150,300))
            plt.yticks((-300,-150,0,150,300))
        plt.xlabel(r"x (kpc h$^{-1}$)")
        plt.ylabel(r"y (kpc h$^{-1}$)")
        plt.tight_layout()
        plt.show()

    def plot_pretty_cut_gas_halo(self,num=0,cut_LLS=17,cut_DLA=20.3):
        """
        Plots a pretty (high-resolution) picture of the grid around a halo.
        """
        cut_grid=np.array(self.sub_gas_grid[num])
        ind=np.where(cut_grid < cut_LLS)
        cut_grid[ind]=10
        ind2=np.where((cut_grid < cut_DLA)*(cut_grid > cut_LLS))
        cut_grid[ind2]=17.
        ind3=np.where(cut_grid > cut_DLA)
        cut_grid[ind3]=20.3
        maxdist = self.sub_radii[num]
        plt.imshow(cut_grid,origin='lower',extent=(-maxdist,maxdist,-maxdist,maxdist),vmin=10,vmax=20.3)
        plt.xlabel(r"x (kpc h$^{-1}$)")
        plt.xlabel(r"y (kpc h$^{-1}$)")
        plt.tight_layout()
        plt.show()

    def plot_pretty_gas_halo(self,num=0):
        """
        Plots a pretty (high-resolution) picture of the grid around a halo.
        """
        self.plot_pretty_something(num,self.sub_gas_grid[num],"log$_{10}$ N$_{H}$ (cm$^{-2}$)")

    def plot_radial_profile(self,minM=3e11,maxM=1e12,minR=0,maxR=20.):
        """Plots the radial density of neutral hydrogen (and possibly gas) for a given halo,
        stacking several halo profiles together."""
        Rbins=np.linspace(minR,maxR,20)
        try:
            aRprof=[self.get_stacked_radial_profile(minM,maxM,Rbins[i],Rbins[i+1]) for i in xrange(0,np.size(Rbins)-1)]
            plt.plot(Rbins[0:-1],aRprof,color=acol, ls=astyle,label="HI")
            #If we didn't load the HI grid this time
        except AttributeError:
            pass
        #Gas profiles
        try:
            agRprof=[self.get_stacked_radial_profile(minM,maxM,Rbins[i],Rbins[i+1],True) for i in xrange(0,np.size(Rbins)-1)]
            plt.plot(Rbins[0:-1],agRprof,color="brown", ls=astyle,label="Gas")
        except AttributeError:
            pass
        plt.xlabel(r"R (kpc h$^{-1}$)")
        plt.ylabel(r"Density $N_{HI}$ (kpc$^{-1}$)")
        plt.legend(loc=1)
        plt.tight_layout()
        plt.show()


class PrettyBox(halohi.BoxHI,PrettyHalo):
    """
    As above but for the whole box grid
    """
    def __init__(self,snap_dir,snapnum,reload_file=False,skip_grid=None,savefile=None):
        halohi.BoxHI.__init__(self,snap_dir,snapnum,reload_file=False,skip_grid=None,savefile=None)


class PrettyTotalHI(halohi.TotalHaloHI):
    """Derived class for plotting total nHI frac and total nHI mass
    against halo mass"""
    def plot_totalHI(self,color="black",label=""):
        """Make the plot of total neutral hydrogen density in a halo:
            Figure 9 of Tescari & Viel 2009"""
        #Plot.
        plt.loglog(self.mass,self.nHI,'o',color=color,label=label)
        #Axes
        plt.xlabel(r"Mass ($M_\odot$ h$^{-1}$)")
        plt.ylabel("HI frac")
        plt.xlim(1e9,5e12)

    def plot_MHI(self,color="black",label=""):
        """Total M_HI vs M_halo"""
        #Plot.
        plt.loglog(self.mass,self.MHI,'o',color=color)
        #Make a best-fit curve.
        ind=np.where(self.MHI > 0.)
        logmass=np.log10(self.mass[ind])-12
        loggas=np.log10(self.MHI[ind])
        ind2=np.where(logmass > -2)
        (alpha,beta)=scipy.polyfit(logmass[ind2],loggas[ind2],1)
        mass_bins=np.logspace(np.log10(np.min(self.mass)),np.log10(np.max(self.mass)),num=100)
        fit= 10**(alpha*(np.log10(mass_bins)-12)+beta)
        plt.loglog(mass_bins,fit, color=color,label=label+r"$\alpha$="+str(np.round(alpha,2))+r" $\beta$ = "+str(np.round(beta,2)))
        #Axes
        plt.xlabel(r"Mass ($M_\odot$ h$^{-1}$)")
        plt.ylabel(r"Mass$_{HI}$ ($M_\odot$ h$^{-1}$)")
        plt.xlim(1e9,5e12)

    def plot_gas(self,color="black",label=""):
        """Total M_gas vs M_halo"""
        #Plot.
        plt.loglog(self.mass,self.Mgas,'o',color=color)
        #Make a best-fit curve.
        ind=np.where(self.Mgas > 0.)
        logmass=np.log10(self.mass[ind])-12
        loggas=np.log10(self.Mgas[ind])
        ind2=np.where(logmass > -2)
        (alpha,beta)=scipy.polyfit(logmass[ind2],loggas[ind2],1)
        mass_bins=np.logspace(np.log10(np.min(self.mass)),np.log10(np.max(self.mass)),num=100)
        fit= 10**(alpha*(np.log10(mass_bins)-12)+beta)
        plt.loglog(mass_bins,fit, color=color,label=label+r"$\alpha$="+str(np.round(alpha,2))+r" $\beta$ = "+str(np.round(beta,2)))
        #Axes
        plt.xlabel(r"Mass ($M_\odot$ h$^{-1}$)")
        plt.ylabel(r"Mass$_{gas}$ ($M_\odot$ h$^{-1}$)")
        plt.xlim(1e9,5e12)


class TotalHIPlots:
    """Class for plotting functions from PrettyHaloHI"""
    def __init__(self,base,snapnum,minpart=400):
        #Get paths
        gdir=path.join(base,"Gadget")
        adir=path.join(base,"Arepo_ENERGY")
        #Load data
        self.atHI=PrettyTotalHI(adir,snapnum,minpart)
        self.atHI.save_file()
        self.gtHI=PrettyTotalHI(gdir,snapnum,minpart)
        self.gtHI.save_file()

    def plot_totalHI(self):
        """Make the plot of total neutral hydrogen density in a halo:
            Figure 9 of Tescari & Viel 2009"""
        #Plot.
        self.gtHI.plot_totalHI(color=gcol,label="Gadget")
        self.atHI.plot_totalHI(color=acol,label="Arepo")
        #Axes
        plt.legend(loc=4)
        plt.tight_layout()
        plt.show()

    def plot_MHI(self):
        """Make the plot of total neutral hydrogen mass in a halo:
            Figure 9 of Tescari & Viel 2009"""
        #Plot.
        self.gtHI.plot_MHI(color=gcol,label="Gadget")
        self.atHI.plot_MHI(color=acol,label="Arepo")
        #Axes
        plt.legend(loc=0)
        plt.tight_layout()
        plt.show()

    def plot_gas(self):
        """Plot total gas mass in a halo"""
        #Plot.
        self.gtHI.plot_gas(color=gcol,label="Gadget")
        self.atHI.plot_gas(color=acol,label="Arepo")
        #Axes
        plt.legend(loc=0)
        plt.tight_layout()
        plt.show()



class HaloHIPlots:
    """
    This class contains functions for plotting all the plots in
    Tescari and Viel which are derived from the grid of HI density around the halos.
    These are figs 10-13
    """
    def __init__(self,base,snapnum,minpart=400,minplot=1e9, maxplot=2e12,reload_file=False,skip_grid=None):
        #Get paths
        self.gdir=path.join(base,"Gadget")
        self.adir=path.join(base,"Arepo_ENERGY")
        #Get data
        self.ahalo=PrettyHalo(self.adir,snapnum,minpart,reload_file=reload_file,skip_grid=skip_grid)
#         self.ahalo.save_file()
        self.ghalo=PrettyHalo(self.gdir,snapnum,minpart,reload_file=reload_file,skip_grid=skip_grid)
#         self.ghalo.save_file()
        self.minplot=minplot
        self.maxplot=maxplot

    def plot_sigma_DLA_model(self,DLA_cut=20.3,DLA_upper_cut=42.):
        """Plot my analytic model for the DLAs"""
        mass=np.logspace(np.log10(np.min(self.ahalo.sub_mass)),np.log10(np.max(self.ahalo.sub_mass)),num=100)
        #Plot Analytic Fit
#         ap=self.ahalo.get_sDLA_fit()
#         gp=self.ghalo.get_sDLA_fit()
        ap=arepo_halo_p[self.ahalo.snapnum]
        gp=gadget_halo_p[self.ghalo.snapnum]
        asfit=self.ahalo.sDLA_analytic(mass,ap,DLA_cut)-self.ahalo.sDLA_analytic(mass,ap,DLA_upper_cut)
        gsfit=self.ghalo.sDLA_analytic(mass,gp,DLA_cut)-self.ghalo.sDLA_analytic(mass,gp,DLA_upper_cut)
        print "Arepo: ",ap
        print "Gadget: ",gp
        plt.loglog(mass,asfit,color=acol,ls=astyle)
        plt.loglog(mass,gsfit,color=gcol,ls=gstyle)

    def plot_sigma_DLA_median(self, DLA_cut=20.3,DLA_upper_cut=42.):
        """Plot the median and scatter of sigma_DLA against mass."""
        mass=np.logspace(np.log10(np.min(self.ahalo.sub_mass)),np.log10(np.max(self.ahalo.sub_mass)),num=7)
        abin_mass = np.empty(np.size(mass)-1)
        gbin_mass = np.empty(np.size(mass)-1)
        abin_mass = halohi.calc_binned_median(mass,self.ahalo.sub_mass, self.ahalo.sub_mass)
        gbin_mass = halohi.calc_binned_median(mass,self.ghalo.sub_mass, self.ghalo.sub_mass)
        (amed,aloq,aupq)=self.ahalo.get_sigma_DLA_binned(mass,DLA_cut,DLA_upper_cut)
        (gmed,gloq,gupq)=self.ghalo.get_sigma_DLA_binned(mass,DLA_cut,DLA_upper_cut)
        #To avoid zeros
        aloq-=1e-2
        gloq-=1e-2
        #Plot median sigma DLA
        plt.errorbar(abin_mass, amed,yerr=[aloq,aupq],fmt='^',color=acol)
        plt.errorbar(gbin_mass*1.1, gmed,yerr=[gloq,gupq],fmt='s',color=gcol)

    def plot_sigma_DLA(self, DLA_cut=20.3,DLA_upper_cut=42.):
        """Plot sigma_DLA vs mass"""
        self.plot_sigma_DLA_contour(DLA_cut,DLA_upper_cut)
        self.plot_sigma_DLA_median(DLA_cut,DLA_upper_cut)
        self.plot_sigma_DLA_model(DLA_cut,DLA_upper_cut)
        #Plot Axes stuff
        ax=plt.gca()
        ax.set_yscale('log')
        ax.set_xscale('log')
        plt.xlabel(r"Mass ($M_\odot$ h$^{-1}$)")
        plt.ylabel(r"$\sigma_{DLA}$ (kpc$^2$ h$^{-2}$)")
        if DLA_cut == 20.3:
            plt.title(r"DLA cross-section at $z="+pr_num(self.ahalo.redshift,1)+"$")
        if DLA_cut == 17.:
            plt.title(r"LLS cross-section at $z="+pr_num(self.ahalo.redshift,1)+"$")
        plt.xlim(self.minplot,self.maxplot)
        if DLA_cut < 19:
            plt.ylim(ymin=10)
        else:
            plt.ylim(ymin=1)
        #Fits
        plt.tight_layout()
        plt.show()

    def plot_sigma_DLA_contour(self, DLA_cut=20.3,DLA_upper_cut=42.):
        """Plot sigma_DLA against mass."""
        gsigDLA=self.ghalo.get_sigma_DLA(DLA_cut,DLA_upper_cut)
        asigDLA=self.ahalo.get_sigma_DLA(DLA_cut,DLA_upper_cut)
        #Plot sigma DLA
        #As contour
        ind = np.where(gsigDLA > 0)
        (hist,xedges, yedges)=np.histogram2d(np.log10(self.ghalo.sub_mass[ind]),np.log10(gsigDLA[ind]),bins=(30,30))
        xbins=np.array([(xedges[i+1]+xedges[i])/2 for i in xrange(0,np.size(xedges)-1)])
        ybins=np.array([(yedges[i+1]+yedges[i])/2 for i in xrange(0,np.size(yedges)-1)])
        plt.contourf(10**xbins,10**ybins,hist.T,[1,1000],colors=(gcol,gcol2),alpha=0.7)
        ind = np.where(asigDLA > 0)
        (hist,xedges, yedges)=np.histogram2d(np.log10(self.ahalo.sub_mass[ind]),np.log10(asigDLA[ind]),bins=(30,30))
        xbins=np.array([(xedges[i+1]+xedges[i])/2 for i in xrange(0,np.size(xedges)-1)])
        ybins=np.array([(yedges[i+1]+yedges[i])/2 for i in xrange(0,np.size(yedges)-1)])
        plt.contourf(10**xbins,10**ybins,hist.T,[1,1000],colors=(acol,acol2),alpha=0.4)

    def get_rel_sigma_DLA(self,DLA_cut=20.3, DLA_upper_cut=42.,min_sigma=15.):
        """
        Get the change in sigma_DLA for a particular halo.
        and the mass of each halo averaged across arepo and gadget.
        DLA_cut is the column density above which to consider a DLA
        min_sigma is the minimal sigma_DLA to look at (in grid cell units)
        """
        aDLA=self.ahalo.get_sigma_DLA(DLA_cut,DLA_upper_cut)
        gDLA=self.ghalo.get_sigma_DLA(DLA_cut,DLA_upper_cut)
        rDLA=np.empty(np.size(aDLA))
        rmass=np.empty(np.size(aDLA))
        cell_area=(2*self.ahalo.sub_radii[0]/self.ahalo.ngrid[0])**2
        for ii in xrange(0,np.size(aDLA)):
            gg=self.ghalo.identify_eq_halo(self.ahalo.sub_mass[ii],self.ahalo.sub_cofm[ii])
            if np.size(gg) > 0 and aDLA[ii]+gDLA[gg] > min_sigma*cell_area:
                rDLA[ii] = aDLA[ii]-gDLA[gg]
                rmass[ii]=0.5*(self.ahalo.sub_mass[ii]+self.ghalo.sub_mass[gg])
            else:
                rDLA[ii]=np.NaN
                rmass[ii]=np.NaN
        return (rmass,rDLA)


    def plot_rel_sigma_DLA(self):
        """Plot sigma_DLA against mass. Figure 10."""
#         (rmass,rDLA)=self.get_rel_sigma_DLA(17,25)
#         ind=np.where(np.isnan(rDLA) != True)
#         plt.semilogx(rmass[ind],rDLA[ind],'o',color="green",label="N_HI> 17")
        (rmass,rDLA)=self.get_rel_sigma_DLA(20.3,30.)
        ind=np.where(np.isnan(rDLA) != True)
        plt.semilogx(rmass[ind],rDLA[ind],'o',color="blue",label="N_HI> 20.3")
        #Axes
        plt.xlim(self.minplot,self.maxplot)
        plt.xlabel(r"Mass ($M_\odot$ h$^{-1}$)")
        plt.ylabel(r"$\sigma_\mathrm{DLA}$ (Arepo) - $\sigma_\mathrm{DLA}$ (Gadget) (kpc$^2$ h$^{-2}$)")
        plt.legend(loc=0)
        plt.tight_layout()
        plt.show()

    def plot_dN_dla(self,Mmin=1e9,Mmax=1e13):
        """Plots dN_DLA/dz for the halos. Figure 11"""
        mass=np.logspace(np.log10(Mmin),np.log10(Mmax),num=100)
        aDLA_dz_tab = np.empty(np.size(mass))
        gDLA_dz_tab = np.empty(np.size(mass))
        for (i,m) in enumerate(mass):
            aDLA_dz_tab[i] = self.ahalo.get_N_DLA_dz(arepo_halo_p[self.ahalo.snapnum],m)
            gDLA_dz_tab[i] = self.ghalo.get_N_DLA_dz(gadget_halo_p[self.ghalo.snapnum],m)
        plt.loglog(mass,aDLA_dz_tab,color=acol,label="Arepo",ls=astyle)
        plt.loglog(mass,gDLA_dz_tab,color=gcol,label="Gadget",ls=gstyle)
        ax=plt.gca()
        ax.fill_between(mass, 10**(-0.7), 10**(-0.5),color='yellow')
        plt.xlabel(r"Mass ($M_\odot$ h$^{-1}$)")
        plt.ylabel(r"$\mathrm{dN}_\mathrm{DLA} / \mathrm{dz} (> M_\mathrm{tot})$")
#         plt.legend(loc=3)
        plt.xlim(Mmin,1e12)
        plt.ylim(10**(-2),1)
        plt.tight_layout()
        plt.show()
#         print "Arepo mean halo mass: ",self.ahalo.get_mean_halo_mass(arepo_halo_p[self.ahalo.snapnum])/1e10
#         print "Gadget mean halo mass: ",self.ghalo.get_mean_halo_mass(gadget_halo_p[self.ghalo.snapnum])/1e10

    def plot_column_density(self,minN=17,maxN=23.):
        """Plots the column density distribution function. Figures 12 and 13"""
        (aNHI,af_N)=self.ahalo.column_density_function(0.4,minN-1,maxN+1)
        (gNHI,gf_N)=self.ghalo.column_density_function(0.4,minN-1,maxN+1)
        plt.loglog(aNHI,af_N,color=acol, ls=astyle,label="Arepo")
        plt.loglog(gNHI,gf_N,color=gcol, ls=gstyle,label="Gadget")
#         (aNH2,af_NH2)=self.ahalo.column_density_function(0.4,minN-1,maxN+1,grids=1)
#         (gNH2,gf_NH2)=self.ghalo.column_density_function(0.4,minN-1,maxN+1,grids=1)
#         plt.loglog(aNH2,af_NH2,color=acol2, ls=astyle,label="Arepo")
#         plt.loglog(gNH2,gf_NH2,color=gcol2, ls=gstyle,label="Gadget")
        #Make the ticks be less-dense
        #ax=plt.gca()
        #ax.xaxis.set_ticks(np.power(10.,np.arange(int(minN),int(maxN),2)))
        #ax.yaxis.set_ticks(np.power(10.,np.arange(int(np.log10(af_N[-1])),int(np.log10(af_N[0])),2)))
        plt.xlabel(r"$N_\mathrm{HI} (\mathrm{cm}^{-2})$")
        plt.ylabel(r"$f(N) (\mathrm{cm}^2)$")
        plt.title(r"Column density function at $z="+pr_num(self.ahalo.redshift,1)+"$")
        plt.xlim(10**minN, 10**maxN)
        plt.ylim(1e-26,1e-18)
#         plt.legend(loc=0)
        plt.tight_layout()
        plt.show()

    def plot_column_density_breakdown(self,minN=17,maxN=23.):
        """Plots the column density distribution function, broken down into halos. """
#         (aNHI,tot_af_N)=self.ahalo.column_density_function(0.4,minN-1,maxN+1)
        (gNHI,tot_gf_N)=self.ghalo.column_density_function(0.4,minN-1,maxN+1)
        (aNHI,af_N)=self.ahalo.column_density_function(0.4,minN-1,maxN+1,minM=11)
        (gNHI,gf_N)=self.ghalo.column_density_function(0.4,minN-1,maxN+1,minM=11)
        plt.loglog(aNHI,af_N/tot_gf_N,color=acol, ls="-",label="Arepo")
        plt.loglog(gNHI,gf_N/tot_gf_N,color=gcol, ls="-",label="Gadget")
        (aNHI,af_N)=self.ahalo.column_density_function(0.4,minN-1,maxN+1,minM=10,maxM=11)
        (gNHI,gf_N)=self.ghalo.column_density_function(0.4,minN-1,maxN+1,minM=10,maxM=11)
        plt.loglog(aNHI,af_N/tot_gf_N,color=acol, ls="--",label="Arepo")
        plt.loglog(gNHI,gf_N/tot_gf_N,color=gcol, ls="--",label="Gadget")
        (aNHI,af_N)=self.ahalo.column_density_function(0.4,minN-1,maxN+1,minM=9,maxM=10)
        (gNHI,gf_N)=self.ghalo.column_density_function(0.4,minN-1,maxN+1,minM=9,maxM=10)
        plt.loglog(aNHI,af_N/tot_gf_N,color=acol, ls=":",label="Arepo")
        plt.loglog(gNHI,gf_N/tot_gf_N,color=gcol, ls=":",label="Gadget")
        #Make the ticks be less-dense
        #ax=plt.gca()
        #ax.xaxis.set_ticks(np.power(10.,np.arange(int(minN),int(maxN),2)))
        #ax.yaxis.set_ticks(np.power(10.,np.arange(int(np.log10(af_N[-1])),int(np.log10(af_N[0])),2)))
        plt.xlabel(r"$N_\mathrm{HI} (\mathrm{cm}^{-2})$")
        plt.ylabel(r"$f_\mathrm{halo}(N) / f_\mathrm{GADGET} (N) $")
#         plt.title(r"Halo contribution to $f(N)$ at $z="+pr_num(self.ahalo.redshift,1)+"$")
        plt.xlim(10**minN, 10**maxN)
        plt.ylim(1e-2,2)
#         plt.legend(loc=0)
        plt.tight_layout()
        plt.show()

    def plot_radial_profile(self,minM=4e11,maxM=1e12,minR=0,maxR=40.):
        """Plots the radial density of neutral hydrogen for all halos stacked in the mass bin.
        """
        #Use sufficiently large bins
        scale = 10**43
        space=2.*self.ahalo.sub_radii[0]/self.ahalo.ngrid[0]
        if maxR/30. > space:
            Rbins=np.linspace(minR,maxR,20)
        else:
            Rbins=np.concatenate((np.array([minR,]),np.linspace(minR+np.ceil(2.5*space),maxR+space,maxR/np.ceil(space))))
        Rbinc = [(Rbins[i+1]+Rbins[i])/2 for i in xrange(0,np.size(Rbins)-1)]
        Rbinc=[minR,]+Rbinc
        try:
            aRprof=[self.ahalo.get_stacked_radial_profile(minM,maxM,Rbins[i],Rbins[i+1])/scale for i in xrange(0,np.size(Rbins)-1)]
            gRprof=[self.ghalo.get_stacked_radial_profile(minM,maxM,Rbins[i],Rbins[i+1])/scale for i in xrange(0,np.size(Rbins)-1)]
            plt.plot(Rbinc,[aRprof[0],]+aRprof,color=acol, ls=astyle,label="Arepo HI")
            plt.plot(Rbinc,[gRprof[0],]+gRprof,color=gcol, ls=gstyle,label="Gadget HI")
            plt.plot(Rbins,2*math.pi*Rbins*self.ahalo.UnitLength_in_cm*10**20.3/scale,color="black", ls="-.",label="DLA density")
            maxx=np.max((aRprof[0],gRprof[0]))
            #If we didn't load the HI grid this time
        except AttributeError:
            pass
#         #Gas profiles
#         try:
#             agRprof=[self.ahalo.get_stacked_radial_profile(minM,maxM,Rbins[i],Rbins[i+1],True) for i in xrange(0,np.size(Rbins)-1)]
#             ggRprof=[self.ghalo.get_stacked_radial_profile(minM,maxM,Rbins[i],Rbins[i+1],True) for i in xrange(0,np.size(Rbins)-1)]
#             plt.plot(Rbinc,[agRprof[0],]+agRprof,color="brown", ls=astyle,label="Arepo Gas")
#             plt.plot(Rbinc,[ggRprof[0],]+ggRprof,color="orange", ls=gstyle,label="Gadget Gas")
#             maxx=np.max((agRprof[0],ggRprof[0]))
#         except AttributeError:
#             pass
        #Make the ticks be less-dense
        #ax=plt.gca()
        #ax.xaxis.set_ticks(np.power(10.,np.arange(int(minN),int(maxN),2)))
        #ax.yaxis.set_ticks(np.power(10.,np.arange(int(np.log10(af_N[-1])),int(np.log10(af_N[0])),2)))
        plt.xlabel(r"R (kpc h$^{-1}$)")
        plt.ylabel(r"Radial Density ($10^{43}$ cm$^{-1}$)")
        #Crop the frame so we see the DLA cross-over point
        DLAdens=2*math.pi*Rbins[-1]*self.ahalo.UnitLength_in_cm*10**20.3
        if maxx > 20*DLAdens:
            plt.ylim(0,20*DLAdens)
        plt.xlim(minR,maxR)
        plt.legend(loc=1)
        plt.tight_layout()
        plt.show()

    def plot_rel_column_density(self,minN=17,maxN=23.):
        """Plots the column density distribution function. Figures 12 and 13"""
        (aNHI,af_N)=self.ahalo.column_density_function(0.4,minN-1,maxN+1)
        (gNHI,gf_N)=self.ghalo.column_density_function(0.4,minN-1,maxN+1)
        plt.semilogx(aNHI,af_N/gf_N,label="Arepo / Gadget",color=rcol)
        #Make the ticks be less-dense
#         ax=plt.gca()
#         ax.xaxis.set_ticks(np.power(10.,np.arange(int(minN),int(maxN),3)))
        #ax.yaxis.set_ticks(np.power(10.,np.arange(int(np.log10(af_N[-1])),int(np.log10(af_N[0])),2)))
        plt.xlabel(r"$N_\mathrm{HI} (\mathrm{cm}^{-2})$")
        plt.ylabel(r"$ \delta f(N)$")
        plt.xlim(10**minN, 10**maxN)
#         plt.legend(loc=0)
        plt.tight_layout()
        plt.show()

    def plot_halo_mass_func(self):
        """Plots the halo mass function as well as Sheth-Torman. Figure 5."""
        mass=np.logspace(np.log10(self.minplot),np.log10(self.maxplot),51)
        shdndm=[self.ahalo.halo_mass.dndm(mm) for mm in mass]
        adndm=np.empty(50)
        gdndm=np.empty(50)
        for ii in range(0,50):
            adndm[ii]=self.ahalo.get_dndm(mass[ii],mass[ii+1])
            gdndm[ii]=self.ghalo.get_dndm(mass[ii],mass[ii+1])
        plt.loglog(mass,shdndm,color="black",ls='--',label="Sheth-Tormen")
        plt.loglog(mass[0:-1],adndm,color=acol,ls=astyle,label="Arepo")
        plt.loglog(mass[0:-1],gdndm,color=gcol,ls=gstyle,label="Gadget")
        #Make the ticks be less-dense
        ax=plt.gca()
        ax.yaxis.set_ticks(np.power(10.,np.arange(int(np.log10(shdndm[-1])),int(np.log10(shdndm[0])),2)))

        plt.ylabel(r"dn/dM (h$^4$ $M^{-1}_\odot$ Mpc$^{-3}$)")
        plt.xlabel(r"Mass ($M_\odot$ h$^{-1}$)")
        plt.legend(loc=0)
        plt.xlim(self.minplot,self.maxplot)
        plt.tight_layout()
        plt.show()

    def print_halo_fits(self):
        """Prints the fitted parameters for the sDLA model"""
        ap=self.ahalo.get_sDLA_fit()
        gp=self.ghalo.get_sDLA_fit()
        print "Arepo: "
        print self.ahalo.snapnum," : ",ap,","
        print "Gadget: "
        print self.ghalo.snapnum," : ",gp,","
