from playwright.sync_api import sync_playwright
import json
import time

def explorar_pagina(page):
    """Explora la estructura de la página para encontrar los selectores correctos"""
    
    print("\n🔍 EXPLORANDO ESTRUCTURA DE LA PÁGINA...")
    print("="*70)
    
    # 1. Guardar HTML completo
    print("\n1. Guardando HTML completo...")
    with open("weather_html.html", "w", encoding="utf-8") as f:
        f.write(page.content())
    print("   ✓ Guardado en: weather_html.html")
    
    # 2. Captura de pantalla
    print("\n2. Tomando captura de pantalla...")
    page.screenshot(path="weather_screenshot.png", full_page=True)
    print("   ✓ Guardado en: weather_screenshot.png")
    
    # 3. Buscar todos los data-testid
    print("\n3. Buscando atributos data-testid...")
    data_testids = page.evaluate('''() => {
        const elementos = document.querySelectorAll('[data-testid]');
        const resultado = {};
        elementos.forEach(el => {
            const testid = el.getAttribute('data-testid');
            if (!resultado[testid]) {
                resultado[testid] = {
                    count: 0,
                    ejemplo_texto: '',
                    ejemplo_html: ''
                };
            }
            resultado[testid].count++;
            if (!resultado[testid].ejemplo_texto && el.innerText) {
                resultado[testid].ejemplo_texto = el.innerText.substring(0, 100);
                resultado[testid].ejemplo_html = el.outerHTML.substring(0, 300);
            }
        });
        return resultado;
    }''')
    
    print(f"\n   Encontrados {len(data_testids)} data-testid diferentes:")
    for testid, info in sorted(data_testids.items(), key=lambda x: x[1]['count'], reverse=True)[:20]:
        print(f"\n   📌 data-testid=\"{testid}\"")
        print(f"      Cantidad: {info['count']}")
        print(f"      Texto: {info['ejemplo_texto'][:50]}...")
    
    # 4. Buscar clases relacionadas con clima
    print("\n\n4. Buscando clases CSS relacionadas...")
    clases_clima = page.evaluate('''() => {
        const palabras = ['month', 'day', 'temp', 'weather', 'calendar', 'card', 'forecast'];
        const clases = new Set();
        
        document.querySelectorAll('*').forEach(el => {
            if (el.className && typeof el.className === 'string') {
                el.className.split(' ').forEach(clase => {
                    palabras.forEach(palabra => {
                        if (clase.toLowerCase().includes(palabra)) {
                            clases.add(clase);
                        }
                    });
                });
            }
        });
        
        return Array.from(clases).slice(0, 30);
    }''')
    
    print(f"\n   Encontradas {len(clases_clima)} clases relevantes:")
    for clase in clases_clima[:15]:
        print(f"      .{clase}")
    
    # 5. Buscar elementos que contengan temperaturas (números con °)
    print("\n\n5. Buscando elementos con temperaturas...")
    elementos_temp = page.evaluate('''() => {
        const elementos = [];
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        let node;
        while(node = walker.nextNode()) {
            if (node.textContent.includes('°')) {
                const parent = node.parentElement;
                elementos.push({
                    texto: node.textContent.trim(),
                    tag: parent.tagName,
                    clase: parent.className,
                    testid: parent.getAttribute('data-testid'),
                    html: parent.outerHTML.substring(0, 200)
                });
            }
        }
        
        return elementos.slice(0, 10);
    }''')
    
    print(f"\n   Encontrados {len(elementos_temp)} elementos con °:")
    for i, elem in enumerate(elementos_temp, 1):
        print(f"\n   {i}. Texto: {elem['texto']}")
        print(f"      Tag: {elem['tag']}")
        print(f"      Clase: {elem['clase'][:50]}...")
        print(f"      data-testid: {elem['testid']}")
    
    # 6. Buscar la estructura principal del calendario
    print("\n\n6. Buscando estructura del calendario mensual...")
    estructura = page.evaluate('''() => {
        // Selectores posibles para el contenedor principal
        const selectores = [
            '[class*="MonthlyCalendar"]',
            '[class*="Calendar"]',
            'main',
            '[data-testid*="Monthly"]',
            '[data-testid*="Calendar"]',
            'article'
        ];
        
        for (let selector of selectores) {
            const elemento = document.querySelector(selector);
            if (elemento) {
                // Contar hijos
                const hijos = elemento.children.length;
                return {
                    selector: selector,
                    hijos: hijos,
                    html: elemento.outerHTML.substring(0, 500),
                    texto: elemento.innerText.substring(0, 300)
                };
            }
        }
        return null;
    }''')
    
    if estructura:
        print(f"\n   ✓ Contenedor encontrado: {estructura['selector']}")
        print(f"   Elementos hijos: {estructura['hijos']}")
        print(f"\n   Texto del contenedor:\n   {estructura['texto'][:200]}...")
    
    # 7. Guardar todos los selectores encontrados
    print("\n\n7. Guardando reporte completo...")
    reporte = {
        'data_testids': data_testids,
        'clases_clima': clases_clima,
        'elementos_temperatura': elementos_temp,
        'estructura_calendario': estructura
    }
    
    with open("weather_selectores.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    print("   ✓ Guardado en: weather_selectores.json")
    
    # 8. Intentar extraer datos con selectores genéricos
    print("\n\n8. Intentando extracción con selectores genéricos...")
    datos_prueba = page.evaluate('''() => {
        const resultados = [];
        
        // Probar diferentes estrategias
        const estrategias = [
            // Estrategia 1: Buscar por tablas
            () => {
                const tabla = document.querySelector('table');
                if (tabla) {
                    const filas = tabla.querySelectorAll('tr');
                    return {nombre: 'tabla', encontrados: filas.length};
                }
                return null;
            },
            
            // Estrategia 2: Buscar por listas
            () => {
                const listas = document.querySelectorAll('ul li, ol li');
                return {nombre: 'listas', encontrados: listas.length};
            },
            
            // Estrategia 3: Buscar divs que contengan fechas
            () => {
                const divs = Array.from(document.querySelectorAll('div')).filter(div => {
                    const texto = div.innerText;
                    return texto.match(/\d{1,2}\s+(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)/i);
                });
                return {nombre: 'divs_con_fecha', encontrados: divs.length};
            },
            
            // Estrategia 4: Buscar elementos article
            () => {
                const articles = document.querySelectorAll('article');
                return {nombre: 'articles', encontrados: articles.length};
            }
        ];
        
        estrategias.forEach(estrategia => {
            const resultado = estrategia();
            if (resultado) resultados.push(resultado);
        });
        
        return resultados;
    }''')
    
    print("\n   Resultados de extracción genérica:")
    for dato in datos_prueba:
        print(f"      • {dato['nombre']}: {dato['encontrados']} elementos")
    
    print("\n" + "="*70)
    print("EXPLORACIÓN COMPLETADA")
    print("="*70)
    print("\nArchivos generados:")
    print("  1. weather_html.html - HTML completo de la página")
    print("  2. weather_screenshot.png - Captura de pantalla")
    print("  3. weather_selectores.json - Todos los selectores encontrados")
    print("\nRevisa estos archivos para identificar los selectores correctos.")

def main():
    print("="*70)
    print("EXPLORADOR DE SELECTORES - WEATHER.COM")
    print("="*70)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        try:
            print("\n📍 Navegando a Weather.com Madrid...")
            page.goto("https://weather.com/es-ES/tiempo/mensual/l/SPXX0050", 
                     wait_until="domcontentloaded", 
                     timeout=60000)
            
            # Aceptar cookies
            print("🍪 Aceptando cookies...")
            try:
                time.sleep(3)
                if page.query_selector("button#truste-consent-button"):
                    page.click("button#truste-consent-button")
                    time.sleep(2)
                elif page.query_selector("button[class*='consent']"):
                    page.click("button[class*='consent']")
                    time.sleep(2)
                print("   ✓ Cookies aceptadas")
            except Exception as e:
                print(f"   ℹ No se pudo aceptar cookies: {e}")
            
            # Esperar a que cargue la página
            print("\n⏳ Esperando a que cargue el contenido...")
            time.sleep(5)  # Espera adicional para asegurar carga completa
            
            # Explorar la página
            explorar_pagina(page)
            
            print("\n\n" + "="*70)
            print("PRÓXIMOS PASOS:")
            print("="*70)
            print("1. Abre weather_html.html en tu navegador")
            print("2. Presiona F12 para abrir DevTools")
            print("3. Busca (Ctrl+F) palabras como: 'temperatura', '°', fecha")
            print("4. Inspecciona los elementos para ver sus selectores")
            print("5. Revisa weather_selectores.json para ver los data-testid")
            print("\nDime qué selectores encuentras y actualizaré el scraper.")
            
            input("\n\nPresiona Enter para cerrar el navegador...")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            page.screenshot(path="error_explorer.png")
            print("Captura guardada en: error_explorer.png")
        
        finally:
            browser.close()

if __name__ == "__main__":
    main()