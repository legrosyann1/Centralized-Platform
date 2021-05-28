from inventory.models import Change
from backend.send_mail import Email
import pandas as pd
import pathlib, os
from datetime import datetime, timedelta

class updateDevicesToExcel():
    email = Email()
    
    def compareDicts(self, change_date, old_data, new_data) -> dict:
        d1_keys = set(old_data.keys())
        d2_keys = set(new_data.keys())
        intersect_keys = d1_keys.intersection(d2_keys)
        modified = {o : ('old data ---> ' + str(old_data[o]) + '  ||  ' + 'new data ---> ' + str(new_data[o])) for o in intersect_keys if old_data[o] != new_data[o]}
        modified['Change date'] = str(change_date.date())
        modified['Ip address'] = new_data['ip_address']
        modified['Name'] = new_data['name']
        return modified

    def createDataFrame(self, changes) -> pd.DataFrame:
        dt = pd.DataFrame(changes)
        dt = dt.reindex(columns=['Name','Ip address','Change date'] + list([a for a in dt.columns if a != 'Name' and a != 'Ip address' and a != 'Change date']))

        # Applying style
        def highlight_col(val):      
            return ['background-color: yellow' if str(v).find('old data --->') != -1 else '' for v in val]

        styled = dt.style.apply(highlight_col)
        return styled

    def saveDataToExcel(self, path, dataframe):
        path = path + 'weeklyDevicesChanges.xlsx'
        if os.path.isfile(path):
            os.remove(path)
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name='Changes', index=False)
        worksheet = writer.sheets['Changes']
        len_columns = []
        
        for i, col in enumerate(dataframe.columns):
            for c in dataframe.data[col]:
                len_columns.append(len(str(c)))
            
            column_len = max(len_columns)
            worksheet.set_column(i, i, column_len + 2)
            len_columns = []
        writer.save()

    def sendMail(self, path):
        file = open(path + 'weeklyDevicesChanges.xlsx', 'rb')
        self.email.send(addr_to = 'legrosyann1@gmail.com',
          subject = 'Updated Weekly Devices',
          body= 'Hi! your excel file with the updated weekly devices is here!',
          file=file,
          filename='weeklyDevicesChanges.xlsx')
        file.close() 


    def start(self):
        #Init variables
        list_old_data = []
        list_new_data = []
        change_date = []
        changes = []
        path = str(pathlib.Path(__file__).parent.parent.absolute() / 'inventory' / 'files' / 'tasks') + os.sep

        data = Change.objects.filter(created_at__gte = datetime.now()-timedelta(weeks=1))
        if len(data) > 0:
            for c in range(len(data)):
                list_old_data.append(data[c].old_info)
                list_new_data.append(data[c].new_info)
                change_date.append(data[c].created_at)

            for index in range(len(list_old_data)):
                changes.append(self.compareDicts(change_date[index], list_old_data[index], list_new_data[index]))

            dataframe = self.createDataFrame(changes)
            self.saveDataToExcel(path, dataframe)
            self.sendMail(path)
        else:
            self.email.send(addr_to = 'legrosyann1@gmail.com',
                            subject = 'Updated Weekly Devices',
                            body= 'Hi! No changes in devices where detected this week!')
        return 'task completed'