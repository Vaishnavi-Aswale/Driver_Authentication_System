function run(lat,long) {
    // body...
    window.location.href = `map.html?lat=${lat}&long=${long}`
  }

function getDet(){
  var userDataRef = firebase.database().ref(`LMV/${id}/Status`).orderByKey();
  userDataRef.once("value").then(function(snapshot) {
    snapshot.forEach(function(childSnapshot) {
      var key = childSnapshot.key;
      var value=childSnapshot.val().value;
      var loc=childSnapshot.val().loc;
      if (value===0){
        var data={
          'value':1,
          'loc':loc
        }
        var updates={}
        updates[`LMV/${id}/Status/${key}`]=data;
        alert("Vehicle in Active mode!!!")  
      }
      if (value===1){
        var data={
          'value':0,
          'loc':loc
        }
        var updates={}
        updates[`LMV/${id}/Status/${key}`]=data;
        alert("Vehicle is now in Dormant mode!!!")
      }
      firebase.database().ref().update(updates)
    });
  })
}

var config = {
  apiKey: "AIzaSyBoFHxK7JnnSaRfa5ApRXxZBeMBYzq48-Q",
    authDomain: "proj-db-c86ba.firebaseapp.com",
    databaseURL: "https://proj-db-c86ba.firebaseio.com",
    projectId: "proj-db-c86ba",
    storageBucket: "proj-db-c86ba.appspot.com",
    messagingSenderId: "1013997305358",
    appId: "1:1013997305358:web:26351a8b745ce17c87465f",
    measurementId: "G-LPYZXGQVZ6"
};

firebase.initializeApp(config);

const urlParams = new URLSearchParams(window.location.search);
const id = Number(urlParams.get('id') );

var userDataRef = firebase.database().ref(`LMV/${id}`).orderByKey();
userDataRef.once("value").then(function(snapshot) {
snapshot.forEach(function(childSnapshot) {
  var key = childSnapshot.key;
  var childData = childSnapshot.val();              
  console.log(childData);
  var name_val = childSnapshot.val().Name;
  var name_val2 = childSnapshot.val().LastName;
  var name_val3 = childSnapshot.val().Lat;
  var name_val4 = childSnapshot.val().Long;
  var name_val5 = childSnapshot.val().LicenseNo;
  var name_val6 = childSnapshot.val().Success;
  var name6="locateme"
  var success="Granted"
  if (name_val6){
    console.log("true")
    success="Granted"
  }
  else{
    console.log("F")
    success="Rejected"
  }

  //var id_val = childSnapshot.val().Last Name;

  // $("#name").append("<p>" + name_val + "</p><br>");
  // $("#LastName").append("<p>" + name_val2 + "</p><br>");
  // $("#Lat").append("<p>" + name_val3 + "</p><br>");
  // $("#Long").append("<p>" + name_val4 + "</p><br>");
  // $("#btn").append("<p>"+name6+"</p><br>");
  //$("#id").append(id_val);

  
  //Rohit did changes here
    if (name_val!== undefined){
    $('tbody').append(
    `<tr>
      <td>${name_val}</td>
      <td>${name_val2}</td>
      <td>${name_val5}</td>
      <td>${success}</td>
      <td>${name_val3}</td>
      <td>${name_val4}</td>
      <td>
        <button onclick=run(${name_val3},${name_val4});>View On Map</button>
      </td>
      
      
    </tr>`
    )
  
  }



  


  });
})
