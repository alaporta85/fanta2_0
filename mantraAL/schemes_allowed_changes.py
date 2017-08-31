

schemes = {'343':['P','Dc','Dc','Dc','E','M/C','M/C','E','W/A','A/Pc','W/A'],
           '3412':['P','Dc','Dc','Dc','E','M/C','M/C','E','T','A/Pc','A/Pc'],
           '3421':['P','Dc','Dc','Dc','E','M/C','M/C','E','T/W','T/W','A/Pc'],
           '352':['P','Dc','Dc','Dc','E/W','M/C','M','M/C','E','A/Pc','A/Pc'],
           '442':['P','Dd','Dc','Dc','Ds','E/W','M','M/C','E/W','A/Pc','A/Pc'],
           '433':['P','Dd','Dc','Dc','Ds','M/C','M','M/C','W/A','A/Pc','W/A'],
           '4312':['P','Dd','Dc','Dc','Ds','M/C','M','M/C','T','A/Pc','A/Pc'],
           '4321':['P','Dd','Dc','Dc','Ds','M/C','M','M/C','T/W','T/W','A/Pc'],
           '4231':['P','Dd','Dc','Dc','Ds','M','M/C','T/W','T','T/W','A/Pc'],
           '4411':['P','Dd','Dc','Dc','Ds','E/W','M','M/C','E/W','T','A/Pc'],
           '4222':['P','Dd','Dc','Dc','Ds','M','M','W','T','A','A/Pc']}


allowed_changes = {'Pc':[(['Pc'],'OK'), (['A'],'OK'), (['T'],'m'), (['W'],'m'),
                         (['C'],'m'), (['M'],'m'), (['E'],'m'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                    'A':[(['Pc'],'*'), (['A'],'OK'), (['T'],'m'), (['W'],'m'),
                         (['C'],'m'), (['M'],'m'), (['E'],'m'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                    'T':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'OK'), (['W'],'**'),
                         (['C'],'m'), (['M'],'m'), (['E'],'m'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                   'W1':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'**'), (['W'],'OK'),
                         (['C'],'m'), (['M'],'m'), (['E'],'m'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                   'W2':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'NO'), (['W'],'OK'),
                         (['C'],'NO'), (['M'],'m'), (['E'],'OK'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                    'C':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'NO'), (['W'],'NO'),
                         (['C'],'OK'), (['M'],'OK'), (['E'],'m'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                    'M':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'NO'), (['W'],'NO'),
                         (['C'],'*'), (['M'],'OK'), (['E'],'m'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                    'E':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'NO'), (['W'],'*'),
                         (['C'],'NO'), (['M'],'m'), (['E'],'OK'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                   'Dc':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'NO'), (['W'],'NO'),
                         (['C'],'NO'), (['M'],'NO'), (['E'],'NO'),
                         (['Dc'],'OK'), (['Dd'],'m'), (['Ds'],'m'),
                         (['Por'],'NO')],
                   'Dd':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'NO'), (['W'],'NO'),
                         (['C'],'NO'), (['M'],'NO'), (['E'],'NO'),
                         (['Dc'],'m'), (['Dd'],'OK'), (['Ds'],'m'),
                         (['Por'],'NO')],
                   'Ds':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'NO'), (['W'],'NO'),
                         (['C'],'NO'), (['M'],'NO'), (['E'],'NO'),
                         (['Dc'],'m'), (['Dd'],'m'), (['Ds'],'OK'),
                         (['Por'],'NO')],
                  'Por':[(['Pc'],'NO'), (['A'],'NO'), (['T'],'NO'), (['W'],'NO'),
                         (['C'],'NO'), (['M'],'NO'), (['E'],'NO'),
                         (['Dc'],'NO'), (['Dd'],'NO'), (['Ds'],'NO'),
                         (['Por'],'OK')]}




























