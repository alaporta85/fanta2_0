


schemes = {'343':['Dc','Dc','Dc','E','M/C','M/C','E','W/A','A/Pc','W/A'],
           
          '3412':['Dc','Dc','Dc','E','M/C','M/C','E','T','A/Pc','A/Pc'],
          
          '3421':['Dc','Dc','Dc','E','M/C','M/C','E','T/W','T/W','A/Pc'],
          
           '352':['Dc','Dc','Dc','E/W','M/C','M','M/C','E','A/Pc','A/Pc'],
           
           '442':['Dd','Dc','Dc','Ds','E/W','M','M/C','E/W','A/Pc','A/Pc'],
           
           '433':['Dd','Dc','Dc','Ds','M/C','M','M/C','W/A','A/Pc','W/A'],
           
          '4312':['Dd','Dc','Dc','Ds','M/C','M','M/C','T','A/Pc','A/Pc'],
          
          '4321':['Dd','Dc','Dc','Ds','M/C','M','M/C','T/W','T/W','A/Pc'],
           
          '4231':['Dd','Dc','Dc','Ds','M','M/C','T/W','T','T/W','A/Pc'],
           
          '4411':['Dd','Dc','Dc','Ds','E/W','M','M/C','E/W','T','A/Pc'],
          
          '4222':['Dd','Dc','Dc','Ds','M','M','W','T','A','A/Pc']}


compatible_roles = {'E':['E/W2'],
                      
                    'M':['M/C'],
                      
                    'C':['M/C'],
                      
                    'T':['T/W1'],
                      
                    'W':['E/W2','T/W1','W1/A', 'W1'],
                      
                    'A':['A/Pc','W1/A'],
                      
                    'Pc':['A/Pc']}


malus_roles = {'Por':[],
                
                'Dc':['A/Pc', 'A', 'T', 'T/W1', 'W1', 'E/W2',
                      'W1/A', 'M/C', 'M', 'E', 'Ds', 'Dd'],
               
                'Dd':['A/Pc', 'A', 'T', 'T/W1', 'W1', 'E/W2',
                      'W1/A', 'M/C', 'M', 'E', 'Ds', 'Dc'],
               
                'Ds':['A/Pc', 'A', 'T', 'T/W1', 'W1', 'E/W2',
                      'W1/A', 'M/C', 'M', 'E', 'Dc', 'Dd'],
                
                 'E':['A/Pc', 'A', 'W1/A', 'T', 'T/W1', 'W1', 'M/C', 'M'],
                
                 'M':['A/Pc', 'A', 'W1/A', 'T', 'T/W1', 'W1', 'E', 'E/W2'],
                
                 'C':['A/Pc', 'A', 'W1/A', 'T', 'T/W1', 'W1'],
                
                 'W':['A/Pc', 'A', 'T'],
                
                 'T':['A/Pc', 'A', 'W1'],
                
                 'A':[],
                
                'Pc':[]}





























