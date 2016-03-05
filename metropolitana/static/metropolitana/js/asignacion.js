$(document).ready(function () {
  $('.tableinput').change(function () { sumValues(); });
  $('.ckSelectAll').change(function () {
    if ($(this).is(':checked') == true) {
      var cant = $(this).closest('div').find('.input-group-addon').first().text();
      $(this).closest('div').find('input').first().val(cant);
      $(this).closest('div').find('input').first().prop('disabled', true);
    }
    else
      $(this).closest('div').find('input').first().prop('disabled', false);

    sumValues();
  })
});

function sumValues() {

  $('.table').each(function () {
    var totalasignacionActual = 0;
    var totalcobroActual = 0;
    var totalverifActual = 0;
    $(this).find('input[name=inputentrega]').each(function () {
      if (!isNaN($(this).val()) && $(this).val()!="")
        totalasignacionActual += parseInt($(this).val());
    });
    $(this).find('input[name=inputcobro]').each(function () {
      if (!isNaN($(this).val()) && $(this).val() != "")
        totalcobroActual += parseInt($(this).val());
    });
    $(this).find('input[name=inputverificacion]').each(function () {
      if (!isNaN($(this).val()) && $(this).val() != "")
        totalverifActual += parseInt($(this).val());
    });

    $('#asignacionActual').text(totalasignacionActual);
    $('#cobroActual').text(totalcobroActual);
    $('#verfiActual').text(totalverifActual);

    var asignacion=0;
    var cobro=0;
    var verif=0;

    asignacion = parseInt($('#asignacionPendiente').text());
    cobro = parseInt($('#cobroPendiente').text());
    verif = parseInt($('#verfPendiente').text());

    $('#asignacionTotal').text(totalasignacionActual+asignacion);
    $('#cobroTotal').text(totalcobroActual+cobro);
    $('#verfTotal').text(totalverifActual+verif);

  });
}
function selectAll(control) {
  if (control.checked) {
    alert("cheked");
  }
}


function obtener_barrios(zona_id) {

            $.ajax({

                url: "{% url 'get_zonas' %}",
                type: 'POST',
                data: zona_id,
                beforeSend: function() {

                    $("#msg").empty().append("<span class='alert'>Cargando...</span>");

                },
                success: function(data) {
                    $("table").empty()
                    //for (var i = 0; i < data.length; i++){
                        alert(data);
                   // }
                }
            });

        }
