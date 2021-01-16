
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


function runFunc(){

    //var id_val = childSnapshot.val().Last Name;
    var abcd=document.querySelector("#fname").value;
    console.log(abcd)
  var userDataRef = firebase.database().ref(`LMV/${abcd}`);

  var Pass2=document.querySelector("#lname").value;
  
  userDataRef.once("value").then(function(snapshot) {
    snapshot.forEach(function(childSnapshot) {
      var key = childSnapshot.key;
      var childData = childSnapshot.val();           
      var Pass = childSnapshot.val().Pass;

      if (String(Pass)===Pass2) {
          window.location = `index.html?id=${abcd}`;    
      }
      else{
          console.log ("Not working");
          //window.location="https://www.facebook.com/"
      }
      });
  })

}
