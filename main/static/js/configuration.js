
/* Declaração das variáveis responsáveis pela tradução dos valores na interface */

//Translated keys
const PT_ACCESS_KEYS = 'Chaves de acesso';
const PT_KEYWORDS = 'Palavras-chave';
const PT_ONLY_PT = 'Somente portugues';


// Original keys
const ACCESS_KEYS = 'access_keys';
const KEYWORDS = 'keywords';
const ONLY_PT = 'only_portuguese';

//Translated key array
const PT_ARRAY = [PT_ACCESS_KEYS, PT_KEYWORDS, PT_ONLY_PT];

//Original key array
const EN_ARRAY = [ACCESS_KEYS, KEYWORDS, ONLY_PT];



function config_editor(data){
  const container = document.getElementById("jsoneditor");
  const options = {
    mode: 'tree'
  };
  const editor = new JSONEditor(container, options);

  const initialJson = getTranslatedJson(data, en_to_pt=true)
  editor.set(initialJson);
}

function fowardJson(){
  let modified_json = editor.get();
  PT_ARRAY.forEach(element => {
    if (!(PT_ARRAY in modified_json)){
      alert(`O campo ${element} foi removido do JSON de configuração. Favor realizar a reinserção.`);
      return false;
    }
  });

  let new_json = getTranslatedJson(modified_json, en_to_pt=false);
  document.getElementById('twitter_configuration') = JSON.stringify(new_json);
  return true;
}



function getTranslatedJson(data_json, en_to_pt = true){

  if(en_to_pt){
    translated_language = EN_ARRAY;
    target_language = PT_ARRAY;
  }else{
    translated_language = PT_ARRAY;
    target_language = EN_ARRAY;
  }

  let new_json = {};
  for(let i = 0; i < translated_language.length; i++){
    new_json[target_language[i]] = data_json[translated_language[i]];
  }

  return new_json;


}