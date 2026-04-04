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
        "* Click with the WhatsApp icon to Add our contact to your WhatsApp contacts and continue.\n" +
        "Copy the below order text (block and copy) and paste it manually in WhatsApp, incase If the message disappears/empty:\n=======\n" +
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
  <div class="min-h-screen bg-orange-50 pb-20 font-sans">
    <!-- Hero Header -->
    <header
      class="bg-blue-800 shadow-sm py-10 mb-8 border-b-4 border-orange-500"
    >
      <h1
        class="text-5xl md:text-7xl font-black text-green-600 text-center uppercase tracking-tighter"
      >
        Priyam Foods
      </h1>
      <p class="text-center text-white mt-2 italic">
        South Indian Moms Special | Authentic Tastes & Flavors | Fresh
        Ingredients | Homemade 100% | Order Now!
      </p>
    </header>

    <div class="max-w-4xl mx-auto px-4">
      <!-- Menu Sections -->
      <div v-for="category in menu" :key="category.category" class="mb-10">
        <h2
          class="text-2xl font-bold text-gray-800 mb-4 border-l-4 border-orange-500 pl-3"
        >
          {{ category.category }}
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="item in category.items"
            :key="item.name"
            :class="[
              'p-4 rounded-2xl border-2 transition-all duration-300 flex justify-between items-center bg-white shadow-sm',
              item.quantity > 0
                ? 'border-green-500 bg-green-50'
                : 'border-transparent hover:border-orange-200',
            ]"
          >
            <div>
              <h3 class="font-bold text-lg text-gray-800">{{ item.name }}</h3>
              <p class="text-orange-600 font-semibold">
                €{{ item.price.toFixed(2) }}
              </p>
            </div>

            <div class="flex items-center gap-3 bg-gray-100 rounded-full p-1">
              <button
                @click="item.quantity = Math.max(0, item.quantity - 1)"
                class="w-8 h-8 rounded-full bg-white shadow flex items-center justify-center hover:bg-orange-500 hover:text-white transition"
              >
                -
              </button>
              <span class="w-6 text-center font-bold">{{ item.quantity }}</span>
              <button
                @click="item.quantity++"
                class="w-8 h-8 rounded-full bg-white shadow flex items-center justify-center hover:bg-green-500 hover:text-white transition"
              >
                +
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Checkout Form -->
      <div
        class="bg-white rounded-3xl shadow-xl p-8 mt-12 border border-gray-100"
      >
        <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
          Delivery Details
        </h2>
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <input
              v-model="firstName"
              placeholder="First Name"
              class="w-full p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none"
            />
            <input
              v-model="lastName"
              placeholder="Last Name"
              class="w-full p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none"
            />
          </div>

          <div class="flex items-center gap-2">
            <input
              v-model="whatsapp"
              type="tel"
              placeholder="WhatsApp Number"
              class="flex-1 min-w-0 p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none"
            />
            <div
              class="bg-green-100 rounded-xl cursor-pointer hover:bg-green-200 transition items-center justify-center"
              @click="storeVCF"
              title="Save Contact"
            >
              <div
                class="bg-green-100 rounded-xl cursor-pointer hover:bg-green-200 transition"
                @click="storeVCF"
                title="Save Contact"
              >
                <img
                  src="./assets/vcf.jpg"
                  class="h-full max-h-[42px] object-contain"
                />
              </div>
            </div>
          </div>

          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="w-full p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none"
          />
          <textarea
            v-model="address"
            placeholder="Full Delivery Address & Special requests (like delivery date/time, allergies, etc.)"
            class="w-full p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none h-32"
          ></textarea>

          <button
            @click="submitOrder"
            class="w-full py-5 bg-orange-600 hover:bg-orange-700 text-white text-xl font-bold rounded-2xl shadow-lg transform active:scale-95 transition-all"
          >
            🚀 Send Order via WhatsApp
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
