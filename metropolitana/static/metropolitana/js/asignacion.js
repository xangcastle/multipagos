$(document).ready(function (){
$('#zonas').change(function(){
    obtener_barrios($(this).val());
    obtener_usuarios($(this).val());
    });
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
                url: "/entregas/get_zonas/",
                type: 'POST',
                data: {'zona_id': zona_id},
                success: function(data) {
                    $("table>tbody").empty()
                    var barrios = data[0].barrios;
                    for (var i = 0; i < barrios.length; i++){
                        var barrio = data[0].barrios[i];

                        var row = '<tr>';
                        row += '<td>' + barrio.code + ' - ' + barrio.name + '<input type="hidden" name="barrio_id" value="' + barrio.id + '"/></td>';
                        row += '<td><div class="input-group input-sm"  style="width:180px"><span class="input-group-addon">' + barrio.entregas + '</span><input type="number" name="inputentrega" class="form-control tableinput"><span class="input-group-addon"><input type="checkbox" class="ckSelectAll"/></span></div></td>';
                        row += '<td><div class="input-group input-sm"  style="width:180px"><span class="input-group-addon">' + barrio.cobros + '</span><input type="number" name="inputcobro" class="form-control tableinput" ><span class="input-group-addon"><input type="checkbox" class="ckSelectAll"/></span></div></td>';
                        row += '<td><div class="input-group input-sm"  style="width:180px"><span class="input-group-addon">' + barrio.verificaciones + '</span><input type="number" name="inputverificacion" class="form-control tableinput" ><span class="input-group-addon"><input type="checkbox" class="ckSelectAll"/></span></div></td>';
                        row += '</tr>';
                        $("table>tbody").append(row);
                    }
                    eventos();
                },
            });
        }


function obtener_usuarios(zona_id) {

            $.ajax({
                url: "/entregas/get_users_zona/",
                type: 'POST',
                data: {'zona_id': zona_id},
                success: function(data) {
                    $('#usuarios').empty();
                    $('#usuarios').append('<option value="0">---</option>');
                    for (var i = 0; i < data.length; i++){
                        $('#usuarios').append('<option value="' + data[i].pk + '">' + data[i].fields.username + '</option>');
                    }
                }
            });
        }


function eventos(){
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

    }