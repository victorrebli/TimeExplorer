import pandas as pd
import numpy as np 

class TimeExplorer():

    def __init__(self, verbose = False):
        self.verbose = verbose

    def create_mean(self, data):
        return data.mean(axis=1)  

    def create_sd(self, data):
        return data.std(axis=1)

    def diff_points(self, data):
        return data.diff(periods=1, axis=1)

    def mean_incresce(self, data):
        positive = data >= 0 
        return data[positive].mean(axis=1)

    def mean_decrease(self, data):
        negative = data < 0 
        return data[negative].mean(axis=1)

    def max_incresce(self, data):
        positive = data >= 0 
        return data[positive].max(axis=1)

    def max_decrease(self, data):
        negative = data < 0 
        return data[negative].max(axis=1)

    def std_diff(self, data):
        return data.std(axis=1)


    def mountain_valey(self, data, data_diff):
        dic_mon = dict()
        dic_valley = dict()
        for _exe in range(1, data.shape[1] - 1):
            dic_mon[data.iloc[:, _exe].name] = np.where((data.iloc[:, _exe] > data.iloc[:, _exe - 1]) & (data.iloc[:, _exe] > data.iloc[:, _exe + 1]), 'mountain', 'not')
            dic_valley[data.iloc[:, _exe].name] = np.where((data.iloc[:, _exe] < data.iloc[:, _exe - 1]) & (data.iloc[:, _exe] < data.iloc[:, _exe + 1]), 'valley', 'not')

        def fun_map(x): 
            if (x['mountain'] == 'not') & (x['valley'] == 'not'):
                return 'neither'
            elif x['mountain'] != 'not':
                return 'mountain'
            elif x['valley'] != 'not':
                return 'valley'
            else:
                return 'error'    

        keys = list(dic_mon.keys())
        dic_final = dict()
        for _key in keys:
            dc = pd.concat([pd.DataFrame(dic_mon[_key], columns=['mountain']), pd.DataFrame(dic_valley[_key],columns=['valley'])], axis=1)
            dc_teste = dc.apply(lambda x: fun_map(x), axis=1)
            dic_final[_key] = dc_teste
            
        dat_mask = pd.DataFrame.from_dict(dic_final)    
        dic_diff = dict()

        for _exe in range(1, data_diff.shape[1] - 1):
            dic_diff[data_diff.iloc[:, _exe].name] = np.abs(data_diff.iloc[:, _exe - 1]) + np.abs(data_diff.iloc[:, _exe + 1])

        dat_final = pd.DataFrame.from_dict(dic_diff)
        return dat_final, dat_mask

    def max_mountain(self, data, dat_mask):
        mask = dat_mask == 'mountain' 
        return data[mask].max(axis=1)

    def max_valley(self, data, dat_mask):
        mask = dat_mask == 'valley' 
        return data[mask].max(axis=1)    

    def run(self, data):
        
        xr_mean = self.create_mean(data)
        xr_std = self.create_sd(data)
        xr_diff = self.diff_points(data)
        xr_mean_inc = self.mean_incresce(xr_diff)
        xr_mean_dec = self.mean_decrease(xr_diff)
        xr_max_inc = self.max_incresce(xr_diff)
        xr_max_dec = self.max_decrease(xr_diff)
        xr_std_diff = self.std_diff(xr_diff)
        dat_final, dat_mask = self.mountain_valey(data,xr_diff)
        xr_max_mountain = self.max_mountain(dat_final, dat_mask)
        xr_max_valley = self.max_valley(dat_final, dat_mask)
        
        return {'mean': xr_mean,
                'std': xr_std,
                'diff_mean_increase': xr_mean_inc,
                'diff_mean_decrease': xr_mean_dec,
                'diff_max_increase': xr_max_inc,
                'diff_max_decrease': xr_max_dec,
                'diff_std': xr_std_diff,
                'max_mountain': xr_max_mountain,
                'max_valley': xr_max_valley}