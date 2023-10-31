// Base URL
const BASE_URL = 'http://127.0.0.1:5000/api'

// Given data about a cupcake, generate HTML
function generateCupcakeHTML(cupcake) {
return `
    <div data-cupcake-id=${cupcake.id}>
        <li>
            ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
            <button class="delete-button">X</button>
        </li>
        <img class="cupcake-image"
                src="${cupcake.image}"
                alt="(no image provided)">
    </div>
    `
}

// Put initial cupcakes on page
async function generateInitialCupcakes() {
    console.log('GETTING INITIAL CUPCAKES')
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    console.log('INTIAL CUPCAKES RESPONSE IS: ', response.data)
    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake)
    }
}

// Handle form for adding new cupcakes
$("#new-cupcake-form").on("submit", async function(evt) {
    evt.preventDefault();
    console.log('BEFORE FORM VALS')
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();
    console.log('BEFORE RESPONSE')
    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });
    console.log('RESPONSE IS: ', newCupcakeResponse.data)
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $('#cupcakes-list').append(newCupcake);
    $('#new-cupcake-form').trigger("reset");
}) 

// Handle clicking delete: delete cupcake
$("#cupcakes-list").on("click", ".delete-button", async function(evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
    console.log(cupcakeId);
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(generateInitialCupcakes);