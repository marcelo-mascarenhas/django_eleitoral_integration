function config_editor(data){
  const container = document.getElementById("jsoneditor");
  const options = {};
  const editor = new JSONEditor(container, options);
  const initialJson = {'Chaves de acesso': data['access_keys'],
  'Palavras-chave': data['keywords'],
  'Somente portugues': data['only_portuguese']
  };
  editor.set(initialJson);

}


function fulfillJson(){
  var json = edito.get();
}

function getJSON() {
  var json = editor.get();
  alert(JSON.stringify(json, null, 2));
}