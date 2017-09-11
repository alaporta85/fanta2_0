

schemes = {'343':['Por','Dc','Dc','Dc','E','M/C','M/C','E','W/A','A/Pc','W/A'],
           
          '3412':['Por','Dc','Dc','Dc','E','M/C','M/C','E','T','A/Pc','A/Pc'],
          
          '3421':['Por','Dc','Dc','Dc','E','M/C','M/C','E','T/W','T/W','A/Pc'],
          
           '352':['Por','Dc','Dc','Dc','E/W','M/C','M','M/C','E','A/Pc','A/Pc'],
           
           '442':['Por','Dd','Dc','Dc','Ds','E/W','M','M/C','E/W','A/Pc','A/Pc'],
           
           '433':['Por','Dd','Dc','Dc','Ds','M/C','M','M/C','W/A','A/Pc','W/A'],
           
          '4312':['Por','Dd','Dc','Dc','Ds','M/C','M','M/C','T','A/Pc','A/Pc'],
          
          '4321':['Por','Dd','Dc','Dc','Ds','M/C','M','M/C','T/W','T/W','A/Pc'],
           
          '4231':['Por','Dd','Dc','Dc','Ds','M','M/C','T/W','T','T/W','A/Pc'],
           
          '4411':['Por','Dd','Dc','Dc','Ds','E/W','M','M/C','E/W','T','A/Pc'],
          
          '4222':['Por','Dd','Dc','Dc','Ds','M','M','W','T','A','A/Pc']}


compatible_roles = {'Por':['Por'],
                    
                     'Dc':['Dc'],
                     
                     'Dd':['Dd'],
                     
                     'Ds':['Ds'],
                         
                      'E':['E/W'],
                      
                      'M':['M/C'],
                      
                      'C':['M/C'],
                      
                      'T':['T/W'],
                      
                      'W':['E/W','T/W','W/A'],
                      
                      'A':['A/Pc','W/A'],
                      
                     'Pc':['A/Pc']}


malus_roles = {'Por':[],
                
                'Dc':['Pc', 'A', 'T', 'W1', 'W2', 'C', 'M', 'E', 'Ds', 'Dd'],
               
                'Dd':['Pc', 'A', 'T', 'W1', 'W2', 'C', 'M', 'E', 'Dc', 'Ds'],
               
                'Ds':['Pc', 'A', 'T', 'W1', 'W2', 'C', 'M', 'E', 'Dc', 'Dd'],
                
                 'E':['Pc', 'A', 'T', 'W1', 'C', 'M'],
                
                 'M':['Pc', 'A', 'T', 'W1', 'W2', 'E'],
                
                 'C':['Pc', 'A', 'T', 'W1'],
                
                 'W':['Pc', 'A', 'T'],
                
                 'T':['Pc', 'A', 'W1'],
                
                 'A':[],
                
                'Pc':[]}





























