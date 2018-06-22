function onDelete(){
  var test = document.getElementById("st_id")
	if(test != null){
    if (confirm("Are you sure to delete the script?")) {
        if (confirm("You are going to delete the script Id:"+test.value+". Are you sure?" )) {
          var form = document.getElementById("popUpForm");
          form.elements["ops"].value = "Del";
          form.submit();
        }
    }
  }
}

function onEdit(){
  var test = document.querySelector('input[name="listSelected"]:checked')
	if(test != null){
          $('#myModal1').modal('toggle');
          href="/algotrade/strategyaddview";
          var form = document.getElementById("scForm");
          form.action ="{% url 'website:strategyeditview'"+ test.value +"%}"
          form.elements["hid_script_id"].value = test.value;
          form.elements["operation"].value = "edit";
         //form.submit();
  } else {
    alert("Select one item from list to edit!");
  }
}
function onChange(id){
  var x = document.getElementById(id);
    x.value = x.checked;
}
function change() {
    var u = document.getElementById("my-checkbox");
    var x = document.getElementById("candleTitle");
    var y = document.getElementById("candleProps");
    var z = document.getElementById("candleChkProps");

    if (!u.checked) {
        x.style.display = "block";
        y.style.display = "block";
        z.style.display = "block";
        
    } else {
        x.style.display = "none";
        y.style.display = "none";
        z.style.display = "none";
    }
};
