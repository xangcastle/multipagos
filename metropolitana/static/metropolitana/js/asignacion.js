$(document).ready(function (){
    $('#zonas').change(function(){
        obtener_barrios($(this).val());
        obtener_usuarios($(this).val());
        $('#histogram').remove();
        });
    $('#dtpFecha').datepicker({
        format: "yyyy-mm-dd",
        language: "es"
     });
});


function sumValues() {
  var total_entrega = 0,
      total_cobro = 0,
      total_verificacion = 0;
  $('.table tbody tr').each(function (key, value) {
    if($(value).find('input[name=entrega]').val().trim() != '')
      total_entrega += parseInt($(value).find('input[name=entrega]').val());
    if($(value).find('input[name=cobro]').val().trim() != '')
      total_cobro += parseInt($(value).find('input[name=cobro]').val());
    if($(value).find('input[name=verificacion]').val().trim() != '')
      total_verificacion += parseInt($(value).find('input[name=verificacion]').val());
    if(key == ($('.table tbody tr').length-1)) {
      $('#verfTotal').text(total_verificacion);
      $('#cobroTotal').text(total_cobro);
      $('#asignacionTotal').text(total_entrega);
      $('#horasdistribucion').empty().html(((total_entrega*3)/60).toFixed(1)+' Horas');
      $('#horascobro').empty().html(((total_cobro*15)/60).toFixed(1)+' Horas');
      $('#horasveficicacion').empty().html(((total_verificacion*8)/60).toFixed(1)+' Horas');
      $('#horastotal').empty()
          .html((
              ((total_entrega*3)/60)
              + ((total_cobro*15)/60)
              + ((total_verificacion*8)/60)).toFixed(1)+' Horas');
    }
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
        if (event.which == 13 ) {
            event.preventDefault();
        }
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
