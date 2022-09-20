$(function () {
    $(".place").click(function () {
      $(this).toggleClass("active");
    });
    $(".unbooked").attr("title","Unbooked");
    $(".taken").attr("title","Taken");
  });

  
  const container = document.querySelector('.container')
  const seats = document.querySelectorAll('.row .seat:not(.occupied)')
  const count = document.getElementById('count')
  const price = document.getElementById('price');
  
  container.addEventListener('click', function (e) {
    console.log(e.target)
    if (
      e.target.classList.contains('seat') &&
      !e.target.classList.contains('occupied')
    ) {
      console.log(e.target)
      e.target.classList.toggle('selected')
      updateSelectedCount()
    }
  })
  
  function updateSelectedCount() {
    const selectedSeats = document.querySelectorAll('.row .seat.selected')
    const selectedSeatsCount = selectedSeats.length
    const selectedSeatsPrice = selectedSeats.length * 250;
    count.innerText = selectedSeatsCount;
    price.innerText = selectedSeatsPrice;
  }
  