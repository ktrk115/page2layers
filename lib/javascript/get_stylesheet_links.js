const urls = [];
const styles = document.styleSheets;
for (let i = 0; i < styles.length; i++) {
    urls.push(styles[i].href);
}
return urls