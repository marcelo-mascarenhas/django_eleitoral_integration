def make_unique(mlist):
    answer = []
    for element in mlist:
        if element not in answer:
            answer.append(element)
    
    return answer

def get_word_list(keyword_list):
  query = ""
  iteration_num = 1
  for item in keyword_list:
    
    if iteration_num > 1:
      query+=" OR "
    else:
      iteration_num+=1
    
    query+=f"{item}"

  return query


if __name__ == "__main__":
  pass