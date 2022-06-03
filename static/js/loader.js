function spinner() {

  // place loader texts inside this strings array
  let strings = [
      ""
  ];
  let rand = strings[Math.floor(Math.random()*strings.length)];
  document.getElementById("loader-text").innerHTML = rand;
  let x = document.getElementById("main-spinner");
  x.style.display = "block";

}