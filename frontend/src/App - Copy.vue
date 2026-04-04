<script setup lang="ts">
import { ref, onMounted } from "vue";

const firstName = ref("");
const lastName = ref("");
const whatsapp = ref("");
const email = ref("");
const address = ref("");

interface Item {
  name: string;
  price: number;
  quantity: number;
}

interface MenuCategory {
  category: string;
  items: Item[];
}

const menu = ref<MenuCategory[]>([]);

onMounted(async () => {
  // const response = await fetch(`${import.meta.env.VITE_API_URL}/menu`)
  const response = await fetch(`${(window as any).APP_CONFIG.API_URL}/menu`);
  const menuData = await response.json();

  menu.value = menuData.map((category: any) => ({
    category: category.category,
    items: category.items.map((item: any) => ({
      name: item.name,
      price: Number(item.price),
      quantity: 0,
    })),
  }));
});

async function storeVCF() {
  const vcfContent = `BEGIN:VCARD
VERSION:3.0
FN:Priyam Foods
TEL;TYPE=CELL:+919840606082
EMAIL:priyam_foods@gmail.com
END:VCARD`;
  const blob = new Blob([vcfContent], { type: "text/vcard" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `PriyamFoods.vcf`;
  a.click();
}

async function submitOrder() {
  const selectedItems = menu.value
    .flatMap((category) => category.items)
    .filter((item) => item.quantity > 0);

  if (selectedItems.length === 0) {
    alert("Please select at least one item to order.");
    return;
  }

  const orderItems = selectedItems.map((item) => ({
    name: item.name,
    quantity: item.quantity,
  }));

  if (!whatsapp.value) {
    alert("Error: Please enter your whatsapp number.");
    return;
  }
  const customer = {
    first_name: firstName.value,
    last_name: lastName.value,
    whatsapp_number: whatsapp.value,
    address: address.value,
    email: email.value,
  };

  const order = {
    customer: customer,
    items: orderItems,
  };
  //alert(JSON.stringify(order));
  console.log(JSON.stringify(order));

  const response = await fetch(`${(window as any).APP_CONFIG.API_URL}/order`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(order),
  });

  const data = await response.json();
  //alert(JSON.stringify(data));
  console.log(JSON.stringify(data));

  if (data.whatsapp_link) {
    const confirmOpen = confirm(
      "Your order is ready!\n\n" +
        "WhatsApp will open with your order details pre-filled.\n" +
        "If the message disappears, copy it from below and paste manually:\n\n" +
        data.message,
    );
    if (confirmOpen) {
      window.open(data.whatsapp_link, "_blank");
    }
  } else {
    alert("Couldn't open whatsapp");
  }

  console.log(data);
}
</script>

<template>
  <div class="text-center text-7xl font-bold text-purple-800 mt-20">
    <p>Priyam Foods</p>
    <br />
  </div>

  <table class="table-auto mx-auto text-left text-2xl mb-8">
    <thead>
      <tr>
        <!-- <th class="px-4 py-2">Category</th> -->
        <th class="px-4 py-2">Item</th>
        <th class="px-4 py-2">Price €</th>
        <th class="px-4 py-2">Quantity</th>
      </tr>
    </thead>
    <tbody>
      <template v-for="category in menu" :key="category.category">
        <tr>
          <td colspan="3" class="border px-4 py-2 font-bold text-3xl">
            {{ category.category }}
          </td>
        </tr>
        <tr
          v-for="item in category.items"
          :key="item.name"
          :class="{ 'bg-green-100': item.quantity > 0 }"
        >
          <td class="border px-4 py-2">{{ item.name }}</td>
          <td class="border px-4 py-2">{{ item.price }}</td>
          <td class="border px-4 py-2">
            <button
              @click="item.quantity = Math.max(0, item.quantity - 1)"
              class="px-3 py-1 bg-gray-300 text-white hover:bg-orange-500 rounded-lg transition"
            >
              -
            </button>
            <span class="mx-2">{{ item.quantity }}</span>
            <button
              @click="item.quantity = Math.max(0, item.quantity + 1)"
              class="px-3 py-1 bg-gray-300 text-white hover:bg-green-500 rounded-lg transition"
            >
              +
            </button>
          </td>
        </tr>
      </template>
    </tbody>
  </table>

  <table class="table-auto mx-auto text-left text-2xl mb-8">
    <thead></thead>
    <tbody>
      <tr>
        <td class="border px-4 py-2">
          First Name: <input v-model="firstName" class="border p-2 w-full" />
        </td>
        <td class="border px-4 py-2">
          Last Name: <input v-model="lastName" class="border p-2 w-full" />
        </td>
      </tr>
      <tr>
        <td class="border px-4 py-2">
          Whatsapp:
          <div class="w-full flex items-center">
            <input
              v-model="whatsapp"
              type="tel"
              required
              pattern="[0-9]{8,15}"
              placeholder="Enter your whatsapp number"
              class="border p-2 flex-1 min-w-0"
            /><img
              src="./assets/vcf.jpg"
              alt="Add store contact for whatsapp order"
              title="*Add store contact for whatsapp order"
              class="fit-image w-8 h-8 inline-block ml-2 cursor-pointer"
              @click="storeVCF"
            />
          </div>
        </td>
        <td class="border px-4 py-2">
          Email:
          <input v-model="email" type="email" class="border p-2 w-full" />
        </td>
      </tr>
      <tr>
        <td colspan="2" class="border px-4 py-2">
          Address: <input v-model="address" class="border p-2 w-full" />
        </td>
      </tr>
      <tr>
        <td colspan="2" class="align-middle border px-4 py-2 text-center">
          <button
            @click="submitOrder"
            class="px-6 py-3 bg-blue-500 text-white hover:bg-blue-700 rounded-lg transition"
          >
            Submit Order
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
<style></style>
