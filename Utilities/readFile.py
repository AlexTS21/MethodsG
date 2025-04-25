import csv

def readCovid(file_path, exclude_column, add_id=True):
    result = {}
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        # Initialize lists for each column (excluding the column to omit)
        for header in headers:
            if not header in exclude_column:
              if header == 'CLASCOVID19':
                result['class'] = []
              else:
                result[header] = []
        print(result.keys())
        # Add id column if needed
        if add_id:
            result['id'] = []

        # Populate the dictionary
        for idx, row in enumerate(reader):

            for header in result.keys():
              if header != 'id':
                res = 0
                hd = header
                if header == 'class':
                  hd = 'CLASCOVID19'
                if row[hd] == 'SI':
                  res = 1
                elif row[hd] == '1':
                  res = 1
                elif row[hd] == 'MUJER':
                  res = 1
                elif row[hd] == 'mayor60':
                  res = 1
                elif row[hd] == 'CONFIRMADO':
                  res =1
                result[header].append(res)
            if add_id:
                result['id'].append(idx)

    return result


def read_by_state_covid(exclude, file_path, state, value):
  exclude.append(state)
  data = {}
  with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    reader= csv.DictReader(file)
    headers = reader.fieldnames
    print(headers)
    for header in headers:
      if not header in exclude:
        if header == 'CLASCOVID19':
          data['class'] = []
        else:
          data[header] = []

    data['id'] = []
    cont = 0

    for indx, row in enumerate(reader):
      if row[state] == value:
        data['id'].append(cont)
        cont+=1
        for header in data.keys():
           if header != 'id':
              res = 0
              hd = header
              if header == 'class':
                hd = 'CLASCOVID19'
             # if header =='ENTRESI':
              #  res = row[header]
              if row[hd] == 'SI':
                res = 1
              elif row[hd] == '1':
                res = 1
              elif row[hd] == 'MUJER':
                res = 1
              elif row[hd] == 'mayor60':
                res = 1
              elif row[hd] == 'CONFIRMADO':
                res =1

              data[header].append(res)
  return data


def read_procesed_covid(file_path):
  data = {}
  with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    reader= csv.DictReader(file)
    headers = reader.fieldnames
    for h in headers:
      data[h] = []
    for indx, row in enumerate(reader):
      for header in data.keys():
        if header == 'id':
          data[header].append(int(row[header]))
        else:
          data[header].append(float(row[header]))
  return data


def read_procesed_noID_Diabetes(file_path):
  data = {}
  with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    reader= csv.DictReader(file)
    headers = reader.fieldnames
    for h in headers:
      if h != 'NOT':
        data[h] = []
    data['id'] = []
    print(data.keys())
    for indx, row in enumerate(reader):
      for header in data.keys():
        if header == 'id':
          data[header].append(indx)
        else:
          data[header].append(float(row[header]))
  return data
