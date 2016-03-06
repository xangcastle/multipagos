$(document).ready(function (){
    $('#zonas').change(function(){
        obtener_barrios($(this).val());
        obtener_usuarios($(this).val());
        });
    $('#dtpFecha').datepicker({
        format: "yyyy-dd-mm",
        language: "es"
     });
});

function sumValues() {

  $('.table').each(function () {
    var totalasignacionActual = 0;
    var totalcobroActual = 0;
    var totalverifActual = 0;
    $(this).find('input[name=entrega]').each(function () {
      if (!isNaN($(this).val()) && $(this).val()!="")
        totalasignacionActual += parseInt($(this).val());
    });
    $(this).find('input[name=cobro]').each(function () {
      if (!isNaN($(this).val()) && $(this).val() != "")
        totalcobroActual += parseInt($(this).val());
    });
    $(this).find('input[name=verificacion]').each(function () {
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

    var hordist=0.0;
    var horcobro=0.0;
    var horverif=0.0;
    
    hordist=(totalasignacionActual+asignacion)*3;
    horcobro=(totalcobroActual+cobro)*15;
    horverif=(totalverifActual+verif)*8;
    
    $('#horasdistribucion').text(totalasignacionActual+asignacion);
    $('#horascobro').text(horcobro);
    $('#horasveficicacion').text(horverif);
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
                        row += '<td>' + barrio.code + ' - ' + barrio.name + '<input type="hidden" name="barrio" id="barrio" value="' + barrio.pk + '"/></td>';
                        row += '<td><div class="input-group input-sm"  style="width:180px"><span class="input-group-addon">' + barrio.entregas + '</span><input step="1" min="0" max="' + barrio.entregas + '" type="number" name="entrega" class="form-control tableinput"><span class="input-group-addon"><input type="checkbox" class="ckSelectAll"/></span></div></td>';
                        row += '<td><div class="input-group input-sm"  style="width:180px"><span class="input-group-addon">' + barrio.cobros + '</span><input step="1" min="0" max="' + barrio.cobros + '" type="number" name="cobro" class="form-control tableinput" ><span class="input-group-addon"><input type="checkbox" class="ckSelectAll"/></span></div></td>';
                        row += '<td><div class="input-group input-sm"  style="width:180px"><span class="input-group-addon">' + barrio.verificaciones + '</span><input step="1" min="0" max="' + barrio.verificaciones + '" type="number" name="verificacion" class="form-control tableinput" ><span class="input-group-addon"><input type="checkbox" class="ckSelectAll"/></span></div></td>';
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
                    $('#usuario').empty();
                    $('#usuario').append('<option selected disabled value="0">---</option>');
                    for (var i = 0; i < data.length; i++){
                        $('#usuario').append('<option value="' + data[i].pk + '">' + data[i].fields.username + '</option>');
                    }
                }
            });
        }


function eventos(){
    //PREVENT DEFAULT TABLEINPUTS
    $('.tableinput').keypress(function(event) {
        event.preventDefault();
    });
    $('.tableinput').change(function () { sumValues(); });
    $('.ckSelectAll').change(function () {
        if ($(this).is(':checked') == true) {
        var cant = $(this).closest('div').find('.input-group-addon').first().text();
        $(this).closest('div').find('input').first().val(cant);
        $(this).closest('div').find('input').first().prop('readonly', true);
        }
        else
        $(this).closest('div').find('input').first().prop('readonly', false);

        sumValues();
    })
}