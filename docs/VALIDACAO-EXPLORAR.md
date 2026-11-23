# Validação externa — interface /explorar (protocolo revisado em 23/11/2026)

## Objetivo e escopo

Avaliar se pessoas externas à equipe conseguem consultar e interpretar dados de acidentes de rodovias federais do Ceará usando a interface `/explorar`, sem orientação durante as tarefas. O resultado é **exploratório**, especialmente com amostra pequena e por conveniência: não prova que o produto seja fácil para toda a população, nem que `/explorar` seja melhor que o Swagger.

**Página testada:** https://api-seguranca-viaria-ce.onrender.com/explorar
**Formulário público:** https://docs.google.com/forms/d/e/1FAIpQLScYO5dqllE4L5dsXwMkozAsHMAAKx6R3SFJlDqfUKCRIJj8Kg/viewform
**Registro privado de respostas:** planilha vinculada ao Forms, com acesso restrito. Não publicar seus dados brutos no GitHub.

## Controles de viés

1. **Convite neutro:** não antecipar que a interface é fácil, intuitiva, superior à API ou que a pessoa deve gostar dela. Ex.: "Estamos avaliando uma página de consulta de dados públicos. Tente algumas atividades sem ajuda e conte como foi. Se não conseguir, isso também é útil para o estudo."
2. **Participantes externos:** não incluir integrantes, autores nem pessoas que conheçam a implementação. Buscar perfis variados; anotar apenas perfil amplo e familiaridade prévia com APIs.
3. **Nenhuma intervenção:** não dizer em qual aba clicar, não mostrar o caminho nem corrigir a resposta durante as tarefas. Anotar dificuldades sem orientar. Se a pessoa pedir ajuda, registrar esse fato.
4. **Tarefa objetiva versus opinião:** marcar *acerto do resultado* separadamente da autoavaliação "consegui" e da nota de facilidade. Resposta autodeclarada não é prova de conclusão correta.
5. **Mesmas instruções para todos:** usar as quatro tarefas já presentes no Forms, nessa ordem, sem fornecer respostas de referência.
6. **Versionar a interface:** registrar data, URL, commit ou versão e dispositivo da sessão. Em 23/11 a interface tinha Fortaleza pré-preenchida; na revisão o município passa a iniciar vazio. Respostas anteriores e posteriores a essa mudança devem ser identificadas como versões diferentes e não somadas indiscriminadamente como se as condições fossem idênticas.
7. **Não remover explicações úteis:** textos sobre cobertura da PRF e limites dos dados fazem parte da experiência de uso. A quarta tarefa mede se a pessoa consegue encontrar e compreender uma limitação divulgada na interface, não se ela chega sozinha a uma conclusão científica inédita.
8. **Ano predefinido:** 2025 continua selecionado por padrão. A primeira tarefa **não avalia** a capacidade de alterar o ano. Não alegar isso no relatório.
9. **Disponibilidade:** antes do convite, conferir que a URL pública serve a versão a ser testada. Falha de rede, demora no Render ou indisponibilidade são resultados relevantes, não motivo para marcar a tarefa como concluída.

## Instruções para participante (copiar sem acrescentar dicas)

> Estamos avaliando uma página de consulta a dados públicos. Use o link para tentar as tarefas abaixo sem ajuda e depois responda ao formulário. Não tem problema se alguma tarefa não der certo. Queremos saber o que aconteceu de verdade.
>
> 1. Descubra quantos acidentes foram registrados em Fortaleza em 2025.
> 2. Identifique a rodovia federal com mais acidentes registrados em 2025.
> 3. Identifique um trecho de 10 km entre os que apresentam mais acidentes em 2025.
> 4. Encontre e explique, com suas palavras, uma limitação importante desses dados.
>
> Site: https://api-seguranca-viaria-ce.onrender.com/explorar
> Formulário: https://docs.google.com/forms/d/e/1FAIpQLScYO5dqllE4L5dsXwMkozAsHMAAKx6R3SFJlDqfUKCRIJj8Kg/viewform

## Ficha de observação da sessão

- ID anônimo: P___
- Data e horário (fuso):
- Versão/commit no Render (ou "não confirmado"):
- Dispositivo: celular / computador / outro
- Área geral e experiência prévia com APIs (sem identificar a pessoa):
- Participação voluntária e autorização para citações: sim / não (conforme Forms)
- A pessoa já tinha acessado essa interface? sim / não / não informado
- Fez as tarefas sem ajuda? sim / não — se não, como ocorreu a intervenção?
- Tempo total (apenas se observado):

| Tarefa | Autodeclarou conclusão? | Resultado que informou | Correto? | Observação objetiva |
| :-- | :-- | :-- | :-- | :-- |
| Fortaleza 2025 | sim/não |  | sim/não/não verificável |  |
| Rodovia com mais acidentes, 2025 | sim/não |  | sim/não/não verificável |  |
| Trecho de 10 km, 2025 | sim/não |  | sim/não/não verificável |  |
| Limitação de interpretação | sim/não |  | sim/não/não verificável |  |

- Nota de facilidade informada (0–10):
- Dificuldade ou melhoria (transcrição anonimizada e autorizada):
- Fonte da resposta original, guardada privadamente:
- Evidência anonimizada, se apropriado: `evidencias/...`

**Como conferir acertos:** consultar a API com os mesmos filtros e a versão de dados testada, registrando os resultados de referência em arquivo interno. Para a tarefa 3, mais de um trecho pode ser aceitável, conforme a redação "entre os que apresentam mais acidentes"; não exigir necessariamente o primeiro do ranking. Na tarefa 4, aceitar qualquer limitação relevante e coerente com as fontes; não exigir uma frase exata.

## Depois de coletar

- Preservar respostas originais e consentimentos em local privado; publicar somente agregados ou trechos anonimizados e autorizados. Não publicar nomes, telefones, e-mails, rostos ou a planilha integral.
- Identificar versões da interface; se houver respostas anteriores à revisão, não editar nem reclassificar seus textos originais. Relatar a diferença metodológica.
- Resumir por tarefa: número de pessoas elegíveis, número de acertos verificáveis, dificuldades observadas, nota de facilidade (com n), tempo **apenas se efetivamente medido** e sugestões recebidas.
- Apontar explicitamente o tamanho pequeno da amostra e o recrutamento por conveniência. Evitar conclusões causais ou significância estatística com poucos participantes.
- Vincular cada evidência anônima ao `evidencias.csv` sem duplicar participantes. Registrar no diário as decisões e, só depois de implementar, as melhorias decorrentes do feedback.
- Há registros de testes anteriores ao desenvolvimento do `/explorar`, realizados no Swagger/API. **Não tratá-los como testes da interface visual** nem como comparação controlada entre os dois modos de consulta.
- Para uma comparação Swagger x interface, criar experimento separado, com grupos comparáveis, tarefas equivalentes, ordem e versão controladas; não inferir superioridade a partir de participantes diferentes e condições não controladas.

Use o modelo [`FICHA-RESULTADOS-USABILIDADE.md`](FICHA-RESULTADOS-USABILIDADE.md) para consolidar sem inventar resultados.
