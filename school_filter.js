function init()
{
    function get_school(row)
    {
        const school_column = 1;
        return row.cells[school_column].innerText;
    }
    
    var table = document.getElementById("results")
    var schools = new Set();
    for (var i=1, row; row=table.rows[i]; i++)
    {
        schools.add(get_school(row));
    }
    schools = Array.from(schools);
    schools.sort();
    var school_select = document.getElementById("cb-school");
    for (var i in schools)
    {
        var option = document.createElement('option');
        option.text = option.value = schools[i];
        school_select.add(option);
    }
    
    school_select.onchange = function()
    {
        var school = school_select.value;
        var show_all = school == "all";
        for (var i=1, row; row=table.rows[i]; i++)
        {
            var match = get_school(row) == school;
            row.style.display = (match || show_all) ? "" : "None";
        }
    }
}

init();
