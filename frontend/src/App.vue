<template>
    <div class="screen-container">
        <div class="iphone">
            <div class="iphone-inner">
                <!-- iPhone content -->
                <router-view>
                </router-view>

                <!-- Bottom navigation -->
                <div class="iphone-bottom">
                    <router-link to="/" class="iphone-button router-link"><font-awesome-icon icon="home" /></router-link>
                    <router-link to="/usage" class="iphone-button router-link"><font-awesome-icon icon="line-chart" /></router-link>
                    <router-link to="/advice" class="iphone-button router-link"><font-awesome-icon icon="info-circle" /></router-link>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default defineComponent({
    components: { RouterLink, FontAwesomeIcon },
});
</script>

<style scoped>
.screen-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #096192;
}

.iphone {
    width: 403px;
    height:812px;
    background: #303032;
    border-radius: 35px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

.iphone-inner {
    width: calc(100% - 20px);
    height: calc(100% - 20px);
    border: 5px solid #303032;
    border-radius: 35px;
    overflow: hidden;
    position: relative;
    background: linear-gradient(190deg, #00456B 0.99%, #00456B 125.25%);

}

.iphone-bottom {
    display: flex;
    justify-content: space-around;
    align-items: center;
    position: absolute;
    bottom: 0px;
    width: calc(100%);
    height: calc(9%);
    border-top: 1px solid linear-gradient(190deg, #00456B 0.99%, #00456B 125.25%);
    background: linear-gradient(190deg, #00456B 0.99%, #00456B 125.25%);
}

.iphone-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: none;
    border: none;
    padding: 8px;
    cursor: pointer;
    outline: none;
}

.iphone-button img {
    width: 24px;
    height: 24px;
    margin-bottom: 4px;
}

.router-link {
    text-decoration: none;
    color: white;
}
</style>
