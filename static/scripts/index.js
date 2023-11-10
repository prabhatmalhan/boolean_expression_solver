output_showing = false;

async function get_solution(eq) {
  options = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ equation: eq }),
  };
  p = await fetch("/solve", options);
  console.log(p);
  sol = await p.text();
  console.log(sol);
  return await sol;
}

async function display_result() {
  sol = await get_solution(document.getElementById("floatingInput").value);
  if (output_showing == false) {
    oc = document.createElement("div");
    oc.setAttribute("id", "output_container");
    pd = document.createElement("div");
    pd.setAttribute("id", "output_div");
    out = document.createElement("input");
    out.setAttribute("type", "text");
    out.setAttribute("class", "form-control");
    out.setAttribute("id", "Output");
    out.setAttribute("disabled", "");
    out.value = sol;
    pd.appendChild(out);
    oc.appendChild(pd);
    document.getElementById("body").appendChild(oc);
    output_showing = true;
  } else document.getElementById("Output").value = sol;
}
